import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await login(email, password);
            navigate('/');
        } catch (err) {
            setError('Falha no login. Verifique suas credenciais.');
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="w-full max-w-md bg-slate-900 p-8 rounded-2xl border border-slate-800 shadow-2xl"
            >
                <div className="flex justify-center mb-8">
                    <div className="w-12 h-12 rounded-xl bg-brand-neon flex items-center justify-center font-bold text-slate-900 text-xl">
                        CV
                    </div>
                </div>

                <h2 className="text-2xl font-bold text-center text-white mb-6">Bem-vindo de volta</h2>

                {error && (
                    <div className="bg-red-500/10 text-red-500 p-3 rounded-lg mb-4 text-sm text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-slate-400 text-sm mb-1">Email</label>
                        <input
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:outline-none focus:border-brand-neon transition-colors"
                            placeholder="seu@email.com"
                        />
                    </div>
                    <div>
                        <label className="block text-slate-400 text-sm mb-1">Senha</label>
                        <input
                            type="password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:outline-none focus:border-brand-neon transition-colors"
                            placeholder="••••••••"
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-brand-neon text-slate-900 font-bold py-3 rounded-lg hover:bg-brand-neon/90 transition-colors"
                    >
                        Entrar
                    </button>
                </form>

                <p className="text-center text-slate-500 text-sm mt-6">
                    Não tem uma conta?{' '}
                    <Link to="/signup" className="text-brand-neon hover:underline">
                        Crie agora
                    </Link>
                </p>
            </motion.div>
        </div>
    );
}
