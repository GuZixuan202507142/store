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

// Validate Firebase configuration
const requiredConfig = ['apiKey', 'authDomain', 'projectId', 'storageBucket', 'messagingSenderId', 'appId'];
const missingConfig = requiredConfig.filter(key => !firebaseConfig[key]);

if (missingConfig.length > 0) {
  console.error('Missing Firebase configuration:', missingConfig);
}

// Initialize Firebase
let app = null;
let db = null;

try {
  app = initializeApp(firebaseConfig);
  db = getFirestore(app);
} catch (error) {
  console.error('Failed to initialize Firebase:', error);
}

export { db };

// Initialize Gemini AI
let geminiModel = null;

try {
  const geminiApiKey = import.meta.env.VITE_GEMINI_API_KEY;
  if (!geminiApiKey) {
    throw new Error('VITE_GEMINI_API_KEY is not configured');
  }
  const genAI = new GoogleGenerativeAI(geminiApiKey);
  geminiModel = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
} catch (error) {
  console.error('Failed to initialize Gemini AI:', error);
}

export { geminiModel };

// Chat history functions
export const getChatHistory = (sessionId, callback) => {
    if (!db) {
        console.error('Firebase not initialized');
        callback([]);
        return () => {}; // Return empty unsubscribe function
    }
    
    try {
        const messagesRef = collection(db, `chats/${sessionId}/messages`);
        const q = query(messagesRef, orderBy("timestamp"));
        return onSnapshot(q, (querySnapshot) => {
            const messages = [];
            querySnapshot.forEach((doc) => {
                messages.push({ id: doc.id, ...doc.data() });
            });
            callback(messages);
        }, (error) => {
            console.error('Error fetching chat history:', error);
            callback([]);
        });
    } catch (error) {
        console.error('Error setting up chat history listener:', error);
        callback([]);
        return () => {};
    }
};

export const saveMessage = async (sessionId, message) => {
    if (!db) {
        console.error('Firebase not initialized');
        throw new Error('Database not available');
    }
    
    try {
        const messagesRef = collection(db, `chats/${sessionId}/messages`);
        await addDoc(messagesRef, message);
    } catch (error) {
        console.error('Error saving message:', error);
        throw new Error('Failed to save message');
    }
};
