import React, {useState} from 'react'
import {
    CCollapse,
    CDropdown,
    CDropdownDivider,
    CDropdownItem,
    CDropdownMenu,
    CDropdownToggle,
    CNavbar,
    CNavbarBrand,
    CNavbarNav,
    CNavbarToggler,
    CNavItem,
    CNavLink
} from '@coreui/react'


const UserAvatar = ({userName, size = 36}) => {
    const initial = (userName && userName.trim().length > 0) ? userName.trim()[0].toUpperCase() : '?'

    const stringToHue = (str) => {
        let hash = 0
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash)
            hash = hash & hash
        }
        return Math.abs(hash) % 360
    }

    const hue = stringToHue(userName || 'user')
    const backgroundColor = `hsl(${hue} 50% 28%)` // dark tone
    const style = {
        width: size,
        height: size,
        minWidth: size,
        borderRadius: '50%',
        backgroundColor,
        color: '#ffffff',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 600,
        fontSize: Math.round(size * 0.5),
        userSelect: 'none'
    }

    return <div style={style} title={userName || 'User'}>{initial}</div>
}

function HeaderNavbar({applications = [], userName = ''}) {
    const [visible, setVisible] = useState(false)

    const onLogout = () => {
        window.open("/auth/logout")
    }

    return (
        <CNavbar
            expand="lg"
            colorScheme="dark"
            className="bg-dark navbar-dark"
            style={{paddingLeft: '20px', paddingRight: '20px'}}
        >
            <CNavbarBrand href="#">Render</CNavbarBrand>
            <CNavbarToggler onClick={() => setVisible(!visible)}/>
            <CCollapse className="navbar-collapse" visible={visible}>
                <CNavbarNav>
                    {applications.map((x, idx) => (
                        <CNavItem key={x.url || x.name || idx}>
                            <CNavLink href={x.url}>{x.name}</CNavLink>
                        </CNavItem>
                    ))}
                </CNavbarNav>

                <div className="ms-auto d-flex align-items-center" style={{gap: 12}}>
                    <CDropdown variant="nav-item">
                        <CDropdownToggle
                            caret={false}
                            className="btn btn-link p-0"
                            style={{textDecoration: 'none'}}
                        >
                            <UserAvatar userName={userName}/>
                        </CDropdownToggle>

                        <CDropdownMenu placement="bottom-end" className="py-0">
                            <CDropdownItem disabled className="px-3 py-2">
                                <div style={{fontWeight: 600}}>{userName || 'User'}</div>
                            </CDropdownItem>
                            <CDropdownDivider/>
                            <CDropdownItem onClick={onLogout} className="px-3 py-2">
                                Logout
                            </CDropdownItem>
                        </CDropdownMenu>
                    </CDropdown>
                </div>
            </CCollapse>
        </CNavbar>
    )
}

export default HeaderNavbar
