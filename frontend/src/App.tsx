import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { initializeApp } from 'firebase/app';
import { 
    getAuth, 
    signInWithPopup, 
    GoogleAuthProvider, 
    onAuthStateChanged,
    signOut,
} from 'firebase/auth';
import ChatInterface from './components/ChatInterface';

// Initialize Firebase
const firebaseConfig = {

};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

function App() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            setUser(user);
            console.log(user)
        });
    
        return () => unsubscribe();
    }, []);
    
    const signInWithGoogle = async () => {
        const provider = new GoogleAuthProvider();
        try {
            const result = await signInWithPopup(auth, provider);
            console.log("User signed in:", result.user);
        } catch (error) {
            console.error("Error signing in:", error.code, error.message);
        }
    };
    
    const handleLogout = async () => {
        try {
            await signOut(auth);
            console.log('Logged out successfully');
        } catch (error) {
            console.error('Error logging out:', error);
        }
    };

    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route 
                        path="/" 
                        element={
                            user ? (
                                <Navigate to="/chat" />
                            ) : (
                                <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
                                    <div className="bg-white rounded-2xl p-8 w-full max-w-md text-center space-y-6">
                                        <h1 className="text-4xl font-bold bg-gradient-to-r from-teal-500 to-blue-500 bg-clip-text text-transparent">
                                            Welcome to Statik
                                        </h1>
                                        <p className="text-gray-600">
                                            Sign in to start chatting with your AI assistant
                                        </p>
                                        <button 
                                            onClick={signInWithGoogle}
                                            className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors text-gray-700 font-medium"
                                        >
                                            <img 
                                                src="https://fonts.gstatic.com/s/i/productlogos/googleg/v6/24px.svg" 
                                                alt="Google logo" 
                                                className="w-6 h-6"
                                            />
                                            Sign in with Google
                                        </button>
                                    </div>
                                </div>
                            )
                        } 
                    />
                    <Route 
                        path="/chat" 
                        element={
                            user ? (
                                <ChatInterface user={user} onLogout={handleLogout} />
                            ) : (
                                <Navigate to="/" />
                            )
                        } 
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;