/* Credentials of the Firebase project.
 *
 * These values are not secrets. Firebase web keys only identify the
 * project, they authorise nothing - who may read and write is decided
 * exclusively by firestore.rules. That is why they sit here in plain text
 * and may live in a public repository.
 *
 * Where to find them in the Firebase console:
 *   Project settings (gear) -> General -> Your apps
 *   -> Web app -> SDK setup and configuration -> Config
 *
 * If there is no web app yet, create one (the "</>" icon). Hosting is not
 * needed, the page lives on GitHub Pages.
 */

export const FIREBASE_CONFIG = {
  apiKey: "AIzaSyCy6TTLSFCuWcdv_EbCxzLfR1c8dD5aOwU",
  authDomain: "astronomyfunfactcards.firebaseapp.com",
  projectId: "astronomyfunfactcards",
  storageBucket: "astronomyfunfactcards.firebasestorage.app",
  messagingSenderId: "309174589768",
  appId: "1:309174589768:web:3d58e622c46cfcecc73b7d",
};
