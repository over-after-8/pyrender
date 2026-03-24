import {createRoot} from "react-dom/client";
import React from "react";
import {CButton, CCol, CContainer, CForm, CFormLabel, CRow,} from "@coreui/react";
import CIcon from "@coreui/icons-react";
import {cilTrash, cilX} from "@coreui/icons";
import {CSRFToken} from "./components/utils";

function DeleteView({csrf_token, model}) {
    return (
        <CForm name="deleteForm" method="post" className="p-3">
            <CSRFToken csrf_token={csrf_token}/>
            <CRow className="mb-3">
                <CCol>
                    <CFormLabel className="fw-semibold">
                        Delete {model} item(s)? Are you sure?
                    </CFormLabel>
                </CCol>
            </CRow>

            <div className="d-flex gap-2">
                <CButton color="danger" type="submit">
                    <CIcon icon={cilTrash} className="me-1"/> Delete
                </CButton>

                <CButton
                    color="secondary"
                    variant="outline"
                    type="button"
                    onClick={() => window.history.back()}
                >
                    <CIcon icon={cilX} className="me-1"/> Cancel
                </CButton>
            </div>
        </CForm>
    );
}

function App({title, csrf_token, model}) {
    return (
        <>
            <h4 className="m-0">{title}</h4>
            <CContainer fluid className="p-3">
                <CRow>
                    <CCol xs={12} md={8} lg={6}>
                        <DeleteView csrf_token={csrf_token} model={model}/>
                    </CCol>
                </CRow>
            </CContainer>
        </>

    );
}

const container = document.getElementById("root_container");
const root = createRoot(container);
const title = document.querySelector('meta[name="title"]').content;
const model = document.querySelector('meta[name="model"]')?.content ?? "";
const csrf_token = document.querySelector('meta[name="csrf_token"]').content;

root.render(<App title={title} csrf_token={csrf_token} model={model}/>);
