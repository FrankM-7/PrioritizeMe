import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import React from 'react';
import { List, ListItem, ListItemText, ListItemSecondaryAction, Checkbox, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete'


const MainSection = ({ section, params }) => {
    const [input, setInput] = useState('');
    const [items, setItems] = useState([]);
    const handleAdd = (text) => {
        setItems([...items, { text, completed: false }]);
        axios.post('/api/menu/submenu/data/add', { menuId: section, submenuId: params.name, text: text }, { 'headers': { 'Authorization': `${localStorage.getItem('token')}` } }
        ).then(res => {
            console.log(res);
        }
        ).catch(err => {
            console.log(err);
        }
        )
    }
    const handleDelete = (index) => {
        setItems(items.filter((_, i) => i !== index));
        axios.delete('/api/menu/submenu/data/delete', { data: { menuId: section, submenuId: params.name, text: items[index].text }, 'headers': { 'Authorization': `${localStorage.getItem('token')}` } }
        ).then(res => {
            console.log(res);
        }).catch(err => {
            console.log(err);
        })
    }
    
    const handleToggle = (index) => {
        setItems(items.map((item, i) => {
            if (i === index) {
                return { ...item, completed: !item.completed };
            }
            return item;
        }));
    }

    useEffect(() => {
        if (section === '') {
          return;
        }
        // send in menuId and submenuId to get the submenu data
        axios.get(`/api/menu/submenu/data`, {
          params: { menuId: section, submenuId: params.name },
          headers: { Authorization: `${localStorage.getItem('token')}` }
        }).then(res => {
          setItems(res.data.tasks);
        }).catch(err => {
          console.log('error')
          console.log(err);
        })
      }, [section, params.name])

    return (
        <div>
            <h1>Main Section</h1>

            <div>
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

                <form onSubmit={e => {
                    e.preventDefault();
                    handleAdd(input);
                    setInput('');
                }}>
                    <input value={input} onChange={e => setInput(e.target.value)} />
                </form>


            </div>
        </div>
    );
};

export default MainSection;
