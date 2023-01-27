import axios from 'axios';
import React from 'react';
//import { useNavigate } from 'react-router-dom';

function Register() {
   // const navigate = useNavigate();
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const handleChange = (e) => {
        if(e.target.name === "email") {
            setEmail(e.target.value)
        } else if(e.target.name === "password") {
            setPassword(e.target.value)
        }
    }

    const handleSubmit = (e) => {
        console.log(email, password);
        e.preventDefault();
        axios.post('/api/signup', { email, password })
            .then(res => {
                if(res.data.status === "success"){
                    // navigate('/login');
                    console.log(res.data);
                }
            })
            .catch(err => {
                console.log(err);
            });
    }

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="email" 
                name="email" 
                value={email} 
                onChange={handleChange} 
                placeholder="Email" 
            />
            <input 
                type="password" 
                name="password" 
                value={password} 
                onChange={handleChange} 
                placeholder="Password" 
            />
            <button type="submit">Register</button>
        </form>
    );
}

export default Register;
