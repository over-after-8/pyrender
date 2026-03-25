import {createRoot} from "react-dom/client";
import React from "react";
import {
    CBadge,
    CButton,
    CCard,
    CCardBody,
    CCol,
    CContainer,
    CDropdown,
    CDropdownItem,
    CDropdownMenu,
    CDropdownToggle,
    CFormCheck,
    CRow,
    CTable,
    CTableBody,
    CTableDataCell,
    CTableRow,
} from "@coreui/react";
import CIcon from "@coreui/icons-react";
import {cilArrowLeft} from "@coreui/icons";

function ActionBox({actions}) {
    const keys = Object.keys(actions || {});
    if (keys.length === 0) return null;

    return (
        <CDropdown className="mb-3">
            <CDropdownToggle color="success" variant="outline">
                Actions
            </CDropdownToggle>
            <CDropdownMenu>
                {keys.map((key) => (
                    <CDropdownItem key={key} href={actions[key]}>
                        {key}
                    </CDropdownItem>
                ))}
            </CDropdownMenu>
        </CDropdown>
    );
}

function ShowViewHelper({value, type}) {
    switch (type) {
        case "Boolean":
            return (
                <div>
                    <CFormCheck disabled checked={Boolean(value)}/>
                </div>
            );

        case "Relationship": {
            if (typeof value === "string") {
                return <span>{value}</span>;
            }
            if (Array.isArray(value) && value.length > 0) {
                return (
                    <>
                        {value.map((item, idx) => (
                            <CBadge color="secondary" className="me-2" key={`${idx}_${item}`}>
                                {item}
                            </CBadge>
                        ))}
                    </>
                );
            }
            return <span>-</span>;
        }

        case "JobRunStatus":
            return <CBadge color="secondary" className="me-2">{value}</CBadge>;

        default:
            return <>{value ?? "-"}</>;
    }
}

function ShowView({model}) {
    const actions = model?.actions ?? {};
    const showFields = model?.show_fields ?? [];
    const fieldTypes = model?.field_types ?? {};
    const item = model?.item ?? {};

    return (
        <>
            {Object.keys(actions).length !== 0 && <ActionBox actions={actions}/>}

            <CCard className="mb-3">
                <CCardBody className="p-0">
                    <CTable striped bordered hover responsive className="mb-0">
                        <CTableBody>
                            {showFields.map((field) => (
                                <CTableRow key={field}>
                                    <CTableDataCell style={{width: "30%"}}>
                                        <strong>{field}</strong>
                                    </CTableDataCell>
                                    <CTableDataCell>
                                        <ShowViewHelper value={item[field]} type={fieldTypes[field]}/>
                                    </CTableDataCell>
                                </CTableRow>
                            ))}
                        </CTableBody>
                    </CTable>
                </CCardBody>
            </CCard>

            <CButton color="secondary" variant="outline" onClick={() => window.history.back()}>
                <CIcon icon={cilArrowLeft} className="me-1"/>
                Back
            </CButton>
        </>
    );
}

function App({model, title}) {
    const parsed = typeof model === "string" ? JSON.parse(model) : model;

    return (
        <>

            <CContainer fluid className="p-3">
                <CRow className="mb-3 align-items-center">
                    <CCol>
                        <h4 className="m-0">{title}</h4>
                    </CCol>
                </CRow>
                <CRow>
                    <CCol xs={12}>
                        <ShowView model={parsed}/>
                    </CCol>
                </CRow>
            </CContainer>
        </>

    );
}

const container = document.getElementById("root_container");
const root = createRoot(container);
const title = document.querySelector('meta[name="title"]')?.content ?? "";
const model = document.querySelector('meta[name="model"]')?.content ?? "{}";

root.render(<App title={title} model={model}/>);
