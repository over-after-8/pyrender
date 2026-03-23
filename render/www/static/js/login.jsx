import React from "react"
import {CAlert, CButton, CCard, CCardBody, CCol, CContainer, CForm, CFormInput, CRow} from "@coreui/react"
import {CSRFToken} from "./components/utils"
import {createRoot} from "react-dom/client";

function App({csrf_token, flashed_messages}) {
    flashed_messages = flashed_messages.length > 0 && JSON.parse(flashed_messages) || []
    console.log(flashed_messages)

    return (
        <CContainer className="d-flex align-items-center min-vh-100">
            <CRow className="justify-content-center w-100">
                <CCol md={6} lg={4}>
                    <CCard>
                        <CCardBody>
                            <h3 className="text-center mb-4">Login</h3>
                            {flashed_messages.map((msg, idx) => (
                                <CAlert key={idx} color={"danger"}>
                                    {msg}
                                </CAlert>
                            ))}

                            <CForm action="/auth/login" method="POST">
                                <CSRFToken csrf_token={csrf_token}/>

                                <CFormInput
                                    type="text"
                                    id="username"
                                    name="username"
                                    placeholder="Username"
                                    className="mb-3"
                                    required
                                />

                                <CFormInput
                                    type="password"
                                    id="password"
                                    name="password"
                                    placeholder="Password"
                                    className="mb-3"
                                    required
                                />

                                <CButton type="submit" color="primary" className="w-100">
                                    Login
                                </CButton>
                            </CForm>
                        </CCardBody>
                    </CCard>
                </CCol>
            </CRow>
        </CContainer>
    )
}

const container = document.getElementById('root_container')
const root = createRoot(container)
const logo = document.querySelector('meta[name="logo"]').content
const csrf_token = document.querySelector('meta[name="csrf_token"]').content
const flashed_messages = document.querySelector('meta[name="flashed_messages"]').content

root.render(
    <App csrf_token={csrf_token} flashed_messages={flashed_messages}/>
)