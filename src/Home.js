import axios from 'axios';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SideNav from './SideNav';
import "./App.css"
import MainSection from './MainSection';

const Home = () => {
    const history = useNavigate();
    const [user, setUser] = useState({});
    const [selected, setSelected] = useState({ section: '', params: { name: '' } });

    const handleClick = (section, params) => {
        setSelected({ section: section, params: params });
      };

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
                if (res.data.status === 'error') {
                    history('/login');
                } else {
                    console.log(res.data);
                }
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
            <SideNav onClickMe={handleClick} />
            <div className='Content'>
                <h2>Welcome {user.email}</h2>
                <MainSection className="Content" {...selected} />
            </div>
        </div>
    );
}

export default Home;