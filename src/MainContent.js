import { List, ListItem, ListItemText, ListItemSecondaryAction, Checkbox, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { useState, useEffect } from 'react';
// import axios from 'axios';



const MainContent = ({ todos, toggleTodo, deleteTodo }) => {
    const [items, setItems] = useState([]);
    const [test, setTest] = useState("not working, redeploy");
    const handleAdd = (text) => {
        setItems([...items, { text, completed: false }]);
    }
    const handleDelete = (index) => {
        setItems(items.filter((_, i) => i !== index));
    }
    const handleToggle = (index) => {
        setItems(items.map((item, i) => {
            if (i === index) {
                return { ...item, completed: !item.completed };
            }
            return item;
        }));
    }

    // when the component mounts, fetch the /test
    // route from the backend and set the items
    // state to the response
    // useEffect(() => {
    //     axios.get('/test')
    //         .then(res => { 
    //             console.log(res.data);
    //             setTest(res.data.message);
    //         })
    //         .catch(err => console.log(err));
    // }, []);


    return (
        <div>
            <h1>{test}</h1>
            <List>
                {items.map((item, index) => (
                    <ListItem key={index} button onClick={() => handleToggle(index)}>
                        <Checkbox checked={item.completed} />
                        <ListItemText primary={item.text} style={{ textDecoration: item.completed ? 'line-through' : 'none' }} />
                        <ListItemSecondaryAction>
                            <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(index)}>
                                <DeleteIcon />
                            </IconButton>
                        </ListItemSecondaryAction>
                    </ListItem>
                ))}
            </List>

            <form onSubmit={(event) => {
                event.preventDefault();
                const text = event.target.elements.text.value;
                if (text) {
                    handleAdd(text);
                    event.target.reset();
                }
            }}>
                <input type="text" name="text" />
                <button type="submit">Add</button>
            </form>


        </div>
    );
}

export default MainContent;