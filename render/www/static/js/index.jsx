import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';
import '@coreui/coreui/dist/css/coreui.min.css'
import {createRoot} from "react-dom/client";
import React from "react";
import HeaderNavbar from "./components/header_navbar";
import createApplications from "./components/applications";
import SidebarMenu from "./components/sidebar_menu";
import parseMenu from "./components/menu";


const header_navbar = createRoot(document.getElementById("header_navbar"))
const applications = createApplications(JSON.parse(document.querySelector('meta[name="applications"]').content))
const user = JSON.parse(document.querySelector('meta[name="current_user"]').content)

header_navbar.render(
    <HeaderNavbar applications={applications} userName={user["user_name"]}/>
)

const applicationMenu = JSON.parse(document.querySelector('meta[name="menu"]').content)
const menu = parseMenu(applicationMenu["menu"])
const applicationName = applicationMenu["application_name"]
const sidebar_menu = createRoot(document.getElementById("sidebar_menu"))
sidebar_menu.render(
    <SidebarMenu menu={menu} applicationName={applicationName}></SidebarMenu>
)