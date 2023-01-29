import axios from 'axios';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const history = useNavigate();
    const [user, setUser] = useState({});

    useEffect(() => {
        const token = localStorage.getItem('token');
        if(!token) {
            history('/login');
        } else {
            // get user email from token
            // fetch user data from server
            // set user data in context
            axios.get('/api/validate', { headers: { Authorization: `${token}` } 
            }) .then(res => {
                console.log("it is valid");
            }) .catch(err => {
                console.log(err);
                history('/login');
            })

            axios.get('/api/user', {
                headers: { Authorization: `${token}` }
            }) .then(res => {
                setUser(res.data.user);
            }) .catch(err => {
                console.log(err);
            })
        }
    }, [])

    return (
        <div>
            <h1>Home</h1>
            <h2>Welcome {user.email}</h2>
        </div>
    );
}

export default Home;