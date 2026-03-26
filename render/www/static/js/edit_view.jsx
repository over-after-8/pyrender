import {createRoot} from "react-dom/client";
import React, {useState} from "react";
import {
    CBadge,
    CButton,
    CCard,
    CCardBody,
    CCol,
    CContainer,
    CForm,
    CFormCheck,
    CFormInput,
    CFormLabel,
    CRow,
} from "@coreui/react";
import Select from "react-select";
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";
import {CSRFToken} from "./components/utils";

function dateToISO(dateStr) {
    if (!dateStr) return "";
    return dateStr;
}

function EditFormHelper({name, type, initValue, relationships}) {
    switch (type) {
        case "image_upload": {
            return (
                <div>
                    <CFormLabel htmlFor={`file_${name}`}>Upload file</CFormLabel>
                    <CFormInput type="file" id={`file_${name}`} name={name}/>
                </div>
            );
        }

        case "date": {
            const [value, setValue] = useState(dateToISO(initValue));

            return (
                <div>
                    <input type="hidden" name={name} value={value}/>
                    <Datetime
                        onChange={(v) => {
                            // v can be a moment object or a string
                            const formatted = v && v.format ? v.format("YYYY-MM-DD") : String(v || "");
                            setValue(formatted);
                        }}
                        value={value || ""}
                        dateFormat={"YYYY-MM-DD"}
                        timeFormat={false}
                        inputProps={{className: "form-control"}}
                    />
                </div>
            );
        }

        case "boolean": {
            const [value, setValue] = useState(Boolean(initValue));
            return (
                <div className="d-flex align-items-center">
                    <CFormCheck
                        type="checkbox"
                        checked={value}
                        onChange={() => setValue((v) => !v)}
                        className="me-2"
                    />
                    <input type="hidden" name={name} value={value ? 1 : 0}/>
                </div>
            );
        }

        case "relationship_many": {
            const relOptions = (relationships?.[name] || []).map((item) => ({
                value: item.id,
                label: item.name,
            }));

            const initialSelected = (initValue || []).map((it) => ({
                value: it.id,
                label: it.name,
            }));

            const [selected, setSelected] = useState(initialSelected);

            const onSelectChangeHandler = (selectedItems) => {
                setSelected(selectedItems || []);
            };

            return (
                <>
                    <Select
                        options={relOptions}
                        name={name}
                        closeMenuOnSelect={false}
                        isMulti
                        value={selected}
                        onChange={onSelectChangeHandler}
                    />
                    {(selected || []).map((s, idx) => (
                        <input key={`${name}_hidden_${idx}`} type="hidden" name={`${name}[]`} value={s.value}/>
                    ))}
                </>
            );
        }

        case "relationship_one": {
            const relOptions = (relationships?.[name] || []).map((item) => ({
                value: item.id,
                label: item.name,
            }));

            const initialSelected = (initValue || {value: -1, label: ""}).map((it) => ({
                value: it.id,
                label: it.name,
            }));
            const [selected, setSelected] = useState(initialSelected);
            return (
                <>
                    <Select
                        options={relOptions}
                        name={name}
                        closeMenuOnSelect={true}
                        value={selected}
                        onChange={setSelected}
                    />
                    {(selected || []).map((s, idx) => (
                        <input key={`${name}_hidden_${idx}`} type="hidden" name={`${name}[]`} value={s.value}/>
                    ))}
                </>
            );
        }

        default: {
            const [value, setValue] = useState(initValue == null ? "" : String(initValue));
            return (
                <CFormInput
                    name={name}
                    type="text"
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                />
            );
        }
    }
}

function DisabledEditFormHelper({type, value}) {
    switch (type) {
        case "Boolean":
            return <CFormCheck type="checkbox" checked={Boolean(value)} disabled/>;
        case "Relationship":
            return (
                <div>
                    {(value || []).map((item, idx) => (
                        <CBadge color="primary" className="me-1" key={`${idx}_${item.id || item.name}`}>
                            {item.name || item}
                        </CBadge>
                    ))}
                </div>
            );
        default:
            return <CFormInput type="text" value={value ?? ""} disabled/>;
    }
}

function EditView({model, csrf_token}) {
    const m = model || {};
    const disabledFields = m.disabled_fields || [];
    const editFields = m.edit_fields || [];
    const fieldTypes = m.field_types || {};
    const relationships = m.relationships || {};
    const item = m.item || {};

    return (
        <CRow>
            <CCol xs={12} md={8} lg={6}>
                <CCard>
                    <CCardBody>
                        <CForm name="editForm" method="post" encType="multipart/form-data">
                            <CSRFToken csrf_token={csrf_token}/>

                            {disabledFields.map((field) => (
                                <div className="mb-3" key={`disabled_${field}`}>
                                    <CFormLabel>
                                        <strong>{field}</strong>
                                    </CFormLabel>
                                    <DisabledEditFormHelper
                                        type={fieldTypes[field]}
                                        value={(item[field] && item[field][0]) ?? ""}
                                    />
                                </div>
                            ))}

                            {editFields.map((field) => (
                                <div className="mb-3" key={`edit_${field}`}>
                                    <CFormLabel>
                                        <strong>{field}</strong>
                                    </CFormLabel>
                                    <EditFormHelper
                                        name={field}
                                        type={fieldTypes[field]}
                                        initValue={(item[field] && item[field][0]) ?? ""}
                                        relationships={relationships}
                                    />
                                </div>
                            ))}

                            <div className="d-flex gap-2">
                                <CButton color="primary" type="submit">
                                    Save
                                </CButton>

                                <CButton color="secondary" variant="outline" type="button"
                                         onClick={() => window.history.back()}>
                                    Cancel
                                </CButton>
                            </div>
                        </CForm>
                    </CCardBody>
                </CCard>
            </CCol>
        </CRow>
    );
}

function App({model, title, csrf_token}) {
    const parsed = typeof model === "string" ? JSON.parse(model) : model;
    return (
        <>
            <CContainer fluid={true}>
                <CRow className="mb-3 align-items-center">
                    <CCol>
                        <h4 className="m-0">{title}</h4>
                    </CCol>
                </CRow>
                <EditView model={parsed} csrf_token={csrf_token}/>
            </CContainer>
        </>
    )
}

const container = document.getElementById("root_container");
const root = createRoot(container);
const title = document.querySelector('meta[name="title"]')?.content ?? "";
const model = document.querySelector('meta[name="model"]')?.content ?? "{}";
const csrf_token = document.querySelector('meta[name="csrf_token"]')?.content ?? "";

root.render(<App title={title} model={model} csrf_token={csrf_token}/>);
