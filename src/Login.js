import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const login = () => {
        axios.post('/login', { email, password })
            .then(res => {
                console.log(res)
                if(res.data.status === "success"){
                    navigate('/');
                }
            })
            .catch(err => {
                console.log(err);
            });
    }

    const handleChange = (e) => {
        if(e.target.name === "email") {
            setEmail(e.target.value)
        } else if(e.target.name === "password") {
            setPassword(e.target.value)
        }
    }

    
    return (
        <div>
        <h1>Login</h1>
        <form onSubmit={login}>
            <label>
            Email
            <input 
                type="email" 
                name="email" 
                value={email} 
                onChange={handleChange} 
                placeholder="Email" 
            />

            </label>
            <label>
            Password
            <input 
                type="password" 
                name="password" 
                value={password} 
                onChange={handleChange} 
                placeholder="Password" 
            />
            </label>
            <button type="submit" onClick={login}>Login</button>
        </form>
        </div>
    );
}

export default Login;