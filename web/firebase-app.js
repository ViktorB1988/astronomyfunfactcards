/* Database layer for the online version.
 *
 * Runs as a module and therefore after the editor script. It never touches
 * the editor state directly, only through window.Editor - that way the
 * offline editor (a single file without this module) stays untouched.
 *
 * Layout in the database:
 *   cards/<id>       one document per card: pos, theme, title, text, more.
 *                    `no` deliberately is not stored - it is derived and
 *                    would touch every document on each reorder. Ordering
 *                    happens through `pos`.
 *   config/meta      title, footer and the theme list in its order (which
 *                    determines the order of the card stack).
 *   config/editors   emails allowed to write. Read only by the security
 *                    rules and by this interface; created by hand in the
 *                    console.
 */

import { initializeApp }
  from "https://www.gstatic.com/firebasejs/11.6.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut,
         onAuthStateChanged }
  from "https://www.gstatic.com/firebasejs/11.6.0/firebase-auth.js";
import { getFirestore, collection, doc, getDoc, onSnapshot, orderBy,
         query, writeBatch }
  from "https://www.gstatic.com/firebasejs/11.6.0/firebase-firestore.js";

import { FIREBASE_CONFIG } from "./firebase-config.js";

const E = window.Editor;
const $ = s => document.querySelector(s);
const cloud    = $("#cloud");
const bSignIn  = $("#signin");
/* The save button lives in the form and is rebuilt on every redraw, so it
   has to be looked up fresh rather than held on to. */
const saveButton = () => document.getElementById("formsave");

/* The editor is running; only the database is not wired up yet. If this
   module fails, a usable - if mute - page is left standing. */
/* Only speaks up when something is wrong. In the normal case the cards are
   simply there - a permanent counter next to them says nothing anyone acts
   on. A failure does need somewhere lasting to show: the status line clears
   itself after a few seconds, so "nicht verbunden" would vanish and leave a
   page that looks fine and quietly is not. */
function report(text, kind){
  if (kind !== "error"){ cloud.hidden = true; return; }
  cloud.hidden = false;
  cloud.textContent = text;
  cloud.classList.add("error");
}

if (!E){
  console.error("window.Editor missing - database stays off.");
} else if (!FIREBASE_CONFIG || /HIER_EINTRAGEN/.test(FIREBASE_CONFIG.apiKey || "")){
  report("keine Firebase-Konfiguration", "error");
  E.status("Die Datei firebase-config.js ist noch nicht ausgefüllt. "
         + "Die Seite zeigt den Stand aus facts.json und speichert nirgendwohin.", true);
  E.setWritable(false);
} else {
  start();
}

function start(){
  const app  = initializeApp(FIREBASE_CONFIG);
  const db   = getFirestore(app);
  const auth = getAuth(app);

  const cardsRef = collection(db, "cards");
  const metaRef  = doc(db, "config", "meta");

  /* Last known state of the database, id -> fields. Basis for the diff on
     save: only what actually changed gets written. Otherwise every save
     would cost 170 writes and would overwrite other people's parallel
     changes. */
  let remote = new Map();
  let remoteMeta = null;
  let haveData = false;
  let isEmpty = false;
  let pending = null;        // snapshot waiting because someone is editing
  let user = null;
  let mayWrite = false;

  /* ---------- Sign-in ----------
     Read-only until the sign-in state is settled. Otherwise open fields
     would sit there for a moment during loading, and typing into them
     would achieve nothing - the database rules would reject it anyway. */
  E.setWritable(false);
  bSignIn.hidden = false;
  bSignIn.onclick = async () => {
    if (user){
      if (E.S.dirty && !confirm("Es gibt ungespeicherte Änderungen. Trotzdem abmelden?")) return;
      await signOut(auth);
      return;
    }
    try {
      await signInWithPopup(auth, new GoogleAuthProvider());
    } catch (e){
      if (e.code === "auth/popup-closed-by-user") return;
      if (e.code === "auth/unauthorized-domain"){
        E.status("Diese Adresse ist in Firebase nicht als autorisierte Domain "
               + "eingetragen (Authentication → Settings → Authorized domains).", true);
        return;
      }
      E.status("Anmeldung fehlgeschlagen: " + (e.code || e.message), true);
    }
  };

  onAuthStateChanged(auth, async account => {
    user = account;
    mayWrite = false;
    let darfEinspielen = false;
    if (account){
      const erlaubt = await rights(account);
      mayWrite = erlaubt.write;
      darfEinspielen = erlaubt.write && erlaubt.mayImport;
      bSignIn.textContent = "Abmelden (" + (account.email || "angemeldet") + ")";
      if (!mayWrite){
        E.status(`${account.email} ist nicht als Redaktion eingetragen und kann `
               + `nur lesen. Eintragen lässt sich das in der Firebase-Konsole `
               + `unter config/editors.`, true);
      }
    } else {
      bSignIn.textContent = "Anmelden";
    }
    /* setWritable redraws the form, and the save button is drawn greyed or
       active from `writable` there - nothing to toggle by hand here. */
    E.setWritable(mayWrite);
    E.setImportAllowed(darfEinspielen);
    if (mayWrite && isEmpty) reportEmpty();
  });

  /* The lists live in the database, not in the source: the security rules
     read the same place, and the addresses therefore stay out of a public
     repository. Only signed-in accounts may read the document.

     `emails` decides who may write - that one the rules enforce too.
     `import` only decides who is shown the import button, and is pure
     convenience: anyone who may write can do the same from the console. */
  async function rights(account){
    const mail = (account.email || "").toLowerCase();
    try {
      const d = await getDoc(doc(db, "config", "editors"));
      const data = d.exists() ? d.data() : {};
      return {write: (data.emails || []).includes(mail),
              mayImport: (data.import || []).includes(mail)};
    } catch (e){
      console.warn("config/editors not readable:", e.code || e.message);
      return {write: false, mayImport: false};
    }
  }

  /* ---------- Reading ---------- */
  report("verbindet …");

  onSnapshot(query(cardsRef, orderBy("pos")), snap => {
    const next = new Map();
    snap.forEach(d => next.set(d.id, d.data()));
    remote = next;
    isEmpty = snap.empty;
    haveData = true;
    report(snap.empty ? "Datenbank leer" : `${snap.size} Karten`, "ok");

    if (snap.empty){
      // Take nothing over: the editor keeps showing the bundled state from
      // facts.json, and that is exactly what can then be uploaded.
      reportEmpty();
      return;
    }
    // Do not play our own unconfirmed writes back at ourselves - that
    // would move the cursor while typing.
    if (snap.metadata.hasPendingWrites) return;
    adopt();
  }, failed);

  onSnapshot(metaRef, d => {
    remoteMeta = d.exists() ? d.data() : null;
    if (haveData && !isEmpty && !E.S.dirty) adopt();
  }, failed);

  function adopt(){
    // themes is stored inside the meta document but is a separate concern
    // for the editor - split it off rather than leaving a stray key behind.
    const {themes, ...metaRest} = remoteMeta || {};
    const state = {
      cards: [...remote.entries()].map(([id, k]) => ({id, ...k})),
      themes: remoteMeta ? themes : null,
      meta:   remoteMeta ? metaRest : null
    };
    state.cards.sort((a, b) => (a.pos ?? 0) - (b.pos ?? 0));

    /* Do not cut in while somebody is typing. The snapshot waits until the
       work has been saved or discarded - otherwise half-written sentences
       vanish under their fingers. */
    if (E.S.dirty){
      pending = state;
      E.status("In der Datenbank hat sich etwas geändert. Nach dem Speichern "
             + "wird der neue Stand übernommen.");
      return;
    }
    pending = null;
    E.setState(state);
  }

  function reportEmpty(){
    if (!mayWrite){
      E.status("Die Datenbank ist noch leer. Angezeigt wird der Stand aus "
             + "facts.json. Zum Befüllen anmelden.", true);
      return;
    }
    E.setDirty(true);
    E.status(`Die Datenbank ist leer. „Speichern“ legt die `
           + `${E.S.cards.length} Karten aus facts.json dort an.`);
  }

  function failed(e){
    report("nicht verbunden", "error");
    const t = e.code === "permission-denied"
      ? "Die Sicherheitsregeln lassen das Lesen nicht zu. Sind firestore.rules "
        + "veröffentlicht?"
      : "Datenbank nicht erreichbar: " + (e.code || e.message);
    E.status(t, true);
  }

  /* ---------- Writing ----------
     Two ways in: the button, and reordering or deleting, which write
     through at once. Both end up here. */
  let saving = false;
  let queued = false;

  async function save(auto){
    if (!mayWrite){ E.status("Zum Speichern anmelden.", true); return; }

    /* An immediate write can arrive while the previous one is still in
       flight - drag two rows in quick succession and the second lands
       mid-commit. Do not interleave batches: note it down and run once
       more afterwards, with the state as it is by then. */
    if (saving){ queued = true; return; }
    saving = true;
    const b = saveButton();
    if (b){ b.disabled = true; b.textContent = "speichert …"; }
    try {
      const state = E.getState();
      const n = await push(state);
      E.setDirty(false);
      if (auto){
        E.status(n ? `Gespeichert (${n} ${n === 1 ? "Änderung" : "Änderungen"}).`
                   : "Gespeichert.");
      } else {
        E.status(n ? `${n} ${n === 1 ? "Änderung" : "Änderungen"} gespeichert. `
                   + `${state.cards.length} Karten in der Datenbank.`
                   : "Nichts zu speichern, alles ist schon aktuell.");
      }
      if (pending){ const p = pending; pending = null; E.setState(p); }
    } catch (e){
      const t = e.code === "permission-denied"
        ? "Gespeichert wurde nichts: Dieses Konto darf laut Sicherheitsregeln "
          + "nicht schreiben."
        : "Speichern fehlgeschlagen: " + (e.code || e.message);
      E.status(t, true);
    } finally {
      saving = false;
      // Look it up again: adopting a snapshot may have rebuilt the form.
      const done = saveButton();
      if (done){ done.disabled = !mayWrite; done.textContent = "Speichern"; }
      if (queued){ queued = false; save(auto); }
    }
  }

  /* Hand the editor both ways in. From here on the form shows a
     "Speichern" button, and reordering and deleting write themselves. */
  E.setDatabase({save: () => save(false), auto: () => save(true)});

  /* Diff, not a blanket rewrite. One batch holds at most 500 operations,
     hence the chunking - 170 cards fit in one, but the limit should not
     bite silently later on. */
  async function push(state){
    const ops = [];

    for (const k of state.cards){
      const old = remote.get(k.id);
      if (old
          && old.pos === k.pos && old.theme === k.theme && old.title === k.title
          && old.text === k.text && old.more === k.more) continue;
      ops.push(b => b.set(doc(db, "cards", k.id), {
        pos: k.pos, theme: k.theme, title: k.title,
        text: k.text, more: k.more
      }));
    }

    const keep = new Set(state.cards.map(k => k.id));
    for (const id of remote.keys()){
      if (!keep.has(id)) ops.push(b => b.delete(doc(db, "cards", id)));
    }

    const meta = {...state.meta, themes: state.themes};
    if (JSON.stringify(meta) !== JSON.stringify(remoteMeta || null)){
      ops.push(b => b.set(metaRef, meta));
    }

    for (let i = 0; i < ops.length; i += 400){
      const batch = writeBatch(db);
      ops.slice(i, i + 400).forEach(f => f(batch));
      await batch.commit();
    }
    return ops.length;
  }

  // Ctrl+S is routed by the editor itself: with a database attached it
  // comes here, without one it downloads a file. Nothing to override.
}
