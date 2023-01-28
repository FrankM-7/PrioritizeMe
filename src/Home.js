import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const history = useNavigate();
    useEffect(() => {
        const token = localStorage.getItem('token');
        if(!token) {
          history('/register');
        }
    }, [])

    return (
        <div>
            <h1>Home</h1>
        </div>
    );
}

export default Home;