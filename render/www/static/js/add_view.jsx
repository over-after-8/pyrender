import {createRoot} from "react-dom/client";
import React, {useState} from "react";
import {CSRFToken} from "./components/utils";
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";

import {CButton, CCard, CCardBody, CCol, CContainer, CForm, CFormInput, CFormLabel, CRow,} from "@coreui/react";

import CIcon from "@coreui/icons-react";
import {cilPlus, cilX} from "@coreui/icons";
import Select from "react-select";
import AddFormHelper from "./components/add_form_helper";

function nowWithoutTime() {
    const date = new Date();
    return date.setHours(0, 0, 0, 0);
}

// function TimestampInput({name}) {
//     const [value, setValue] = useState(nowWithoutTime());
//     return (
//         <div className="mb-3">
//             <label className="form-label">{name}</label>
//             <input type="hidden" name={name} value={value}/>
//             <Datetime dateFormat="YYYY-MM-DD" timeFormat="HH:mm" onChange={setValue}/>
//         </div>
//     );
// }




function AddView({model, csrf_token}) {
    console.log(model)
    return (
        <CCard>
            <CCardBody>
                <CForm name="addForm" method="post">
                    <CSRFToken csrf_token={csrf_token}/>
                    {model.add_fields.map((field) => (
                        <AddFormHelper name={field} data_type={model.data_types[field] || "default"}
                                       relationships={model.relationships} select_items={model.select_items}/>
                    ))}

                    <CButton color="success" type="submit" className="me-2">
                        <CIcon icon={cilPlus} className="me-1"/>
                        Add
                    </CButton>

                    <CButton
                        color="danger"
                        variant="outline"
                        type="button"
                        onClick={() => history.back()}
                    >
                        <CIcon icon={cilX} className="me-1"/>
                        Cancel
                    </CButton>
                </CForm>
            </CCardBody>
        </CCard>
    );
}

function App({model, title, csrf_token}) {
    const data = JSON.parse(model);
    return (
        <>
            <CContainer fluid={true}>
                <CRow className="mb-3 align-items-center">
                    <CCol>
                        <h4 className="m-0">{title}</h4>
                    </CCol>
                </CRow>
                <CRow>
                    <CCol md={6}>
                        <AddView model={data} csrf_token={csrf_token}/>
                    </CCol>
                    <CCol md={6}></CCol>
                </CRow>
            </CContainer>
        </>
    );
}

const container = document.getElementById('root_container');
const root = createRoot(container);
const title = document.querySelector('meta[name="title"]').content;
const model = document.querySelector('meta[name="model"]').content;
const csrf_token = document.querySelector('meta[name="csrf_token"]').content;

root.render(
    <App title={title} model={model} csrf_token={csrf_token}/>
);
