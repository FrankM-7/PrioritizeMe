import React, { useState } from 'react';
import './SideNav.css';

const SideNav = () => {
    const [openMenus, setOpenMenus] = useState([]);
    const [menus, setMenus] = useState([
        { name: 'Home', submenus: ['Submenu 1', 'Submenu 2', 'Submenu 3'] },
    ]);

   
    const preAddMenu = () => {
        const newMenuName = prompt("Please enter a name for the new menu:");
        if (menus.filter(m => m.name === newMenuName).length === 0 ) {
            addMenu(newMenuName);
        } else {
            alert("Menu name already exists or you didn't enter a name!");
            preAddMenu();
        }
    }

    const addMenu = (name) => {
        const newMenu = { name: name, submenus: ['Submenu 1', 'Submenu 2', 'Submenu 3'] }
        setMenus([...menus, newMenu])
    }

    const handleClick = (menu) => {
        if (openMenus.includes(menu)) {
            setOpenMenus(openMenus.filter(m => m !== menu));
        } else {
            setOpenMenus([...openMenus, menu]);
        }
    }

    return (
        <nav className="sidenav">
            {/* <ul>
                {menus.map((menu, index) => (
                    <li key={index} onClick={() => handleClick(menu.name)}>
                        <a href="#" className={openMenus.includes(menu.name) ? 'active' : ''}>{menu.name}</a>
                        {openMenus.includes(menu.name) && (
                            <ul>
                                {menu.submenus.map((submenu, subIndex) => (
                                    <li key={subIndex}>
                                        <a href="#" onClick={(event) => {event.stopPropagation()}}>{submenu}</a>
                                    </li>
                                ))}
                                <li key={menu.submenus.length + 1}>
                                    <button onClick={(event) => {
                                        event.stopPropagation();
                                        const newSubmenuName = prompt("Please enter a name for the new submenu:");
                                        if (newSubmenuName) {
                                            const newSubmenus = [...menu.submenus, newSubmenuName];
                                            const newMenus = menus.map(m => {
                                                if (m.name === menu.name) {
                                                    return { ...m, submenus: newSubmenus };
                                                }
                                                return m;
                                            });
                                            setMenus(newMenus);
                                        }
                                    }}>Add Submenu</button>
                                </li>
                            </ul>
                        )}
                    </li>
                ))}
            </ul> */}

            <button onClick={() => {
                preAddMenu();
            }}>Add Menu</button>

        </nav>
    );
}

export default SideNav;