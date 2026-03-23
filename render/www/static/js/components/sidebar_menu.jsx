import React, {useState} from 'react'
import {CNavItem, CNavTitle, CSidebar, CSidebarBrand, CSidebarHeader, CSidebarNav, CSidebarToggler} from '@coreui/react'
import {CIcon} from "@coreui/icons-react";
import {cilLayers} from "@coreui/icons";

const SidebarMenu = ({menu, applicationName}) => {
    console.log(menu)
    const [visible, setVisible] = useState(true)

    return (
        <>
            <CSidebar
                className="border-end"
                visible={visible}
                onVisibleChange={(val) => setVisible(val)}
                style={{height: '100%'}} // ensure sidebar fills parent's height
            >
                <CSidebarHeader className="border-bottom">
                    <CSidebarBrand style={{textDecoration: 'none'}}>{applicationName}</CSidebarBrand>
                </CSidebarHeader>

                <CSidebarNav>
                    {menu.map((cat) => (
                        <React.Fragment key={cat.name}>
                            <CNavTitle>{cat.name}</CNavTitle>
                            {cat.items.map((item, idx) => {
                                return (
                                    <CNavItem href={item.url || '#'} key={`${cat.name}-${idx}`}>
                                        {/* optional icon: if item.icon exists, render CIcon */}
                                        {item.icon ? <CIcon customClassName="nav-icon" icon={item.icon}/> :
                                            <CIcon customClassName="nav-icon" icon={cilLayers}/>}
                                        {item.name}
                                    </CNavItem>
                                )
                            })}
                        </React.Fragment>
                    ))}
                </CSidebarNav>

                <CSidebarToggler onClick={() => setVisible(!visible)}/>
            </CSidebar>

        </>
    )
}

export default SidebarMenu
