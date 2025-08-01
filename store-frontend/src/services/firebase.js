import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc, query, orderBy, onSnapshot } from "firebase/firestore";
import { GoogleGenerativeAI } from "@google/generative-ai";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

// Initialize Gemini through Firebase AI Logic SDK equivalent
// The @google/generative-ai SDK is the modern way to do this
const genAI = new GoogleGenerativeAI("AIzaSyA2-M7sWX18X8unq1Hn1QKHOevUSiw9QRU"); // Using provided Gemini API Key
export const geminiModel = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

// Chat history functions
export const getChatHistory = (sessionId, callback) => {
    const messagesRef = collection(db, `chats/${sessionId}/messages`);
    const q = query(messagesRef, orderBy("timestamp"));
    return onSnapshot(q, (querySnapshot) => {
        const messages = [];
        querySnapshot.forEach((doc) => {
            messages.push({ id: doc.id, ...doc.data() });
        });
        callback(messages);
    });
};

export const saveMessage = async (sessionId, message) => {
    const messagesRef = collection(db, `chats/${sessionId}/messages`);
    await addDoc(messagesRef, message);
};
