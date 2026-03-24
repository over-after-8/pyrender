import {createRoot} from "react-dom/client";
import React, {useState} from "react";
import {
    CBadge,
    CButton,
    CButtonGroup,
    CCard,
    CCardBody,
    CCol,
    CContainer,
    CFormCheck,
    CFormInput,
    CInputGroup,
    CRow,
    CTable,
    CTableBody,
    CTableDataCell,
    CTableHead,
    CTableHeaderCell,
    CTableRow
} from "@coreui/react";
import CIcon from "@coreui/icons-react";
import {cilPencil, cilSearch, cilTrash} from "@coreui/icons";

function ListViewHelper({value, type, row_id}) {
    switch (type) {
        case "Boolean":
            return (
                <CFormCheck
                    disabled
                    checked={Boolean(value)}
                    className="m-0"
                />
            );

        case "Relationship":
            if (typeof value === "string") {
                return (
                    <CBadge color="secondary" className="me-1">
                        {value}
                    </CBadge>
                );
            } else if (Array.isArray(value)) {
                return (
                    <>
                        {value.map((item, idx) => (
                            <CBadge color="secondary" className="me-1" key={`${row_id}_${idx}`}>
                                {item}
                            </CBadge>
                        ))}
                    </>
                );
            } else {
                return <span>-</span>;
            }

        default:
            return <span>{value}</span>;
    }
}


function SearchBox({search_url, keyword, page_size}) {
    const initial = keyword === "null" || keyword == null ? "" : keyword;
    const [kw, setKw] = useState(initial);

    const buildUrl = () => {
        const params = new URLSearchParams();
        if (kw) params.set("keyword", kw);
        params.set("page", "1");
        if (page_size) params.set("page_size", String(page_size));
        return `${search_url}?${params.toString()}`;
    };

    const search = () => {
        window.location.replace(buildUrl());
    };

    const onKeyDown = (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            search();
        }
    };

    return (
        <CRow className="g-2">
            <CCol xs="auto">
                <CInputGroup>
                    <CFormInput
                        id="inputKeyword"
                        value={kw}
                        onChange={(e) => setKw(e.target.value)}
                        onKeyDown={onKeyDown}
                        placeholder="keyword..."
                    />
                </CInputGroup>
            </CCol>
            <CCol xs="auto">
                <CButton color="primary" onClick={search}>
                    Search
                </CButton>
            </CCol>
        </CRow>
    );
}

function AddBox({add_url}) {
    const add = () => {
        window.location.replace(add_url);
    };

    return (
        <CButton color="success" variant="outline" onClick={add}>
            New
        </CButton>
    );
}

function ActionColumn({item}) {
    const btnStyle = {height: "25px", padding: "2px", width: "25px"};

    return (
        <CButtonGroup role="group" size="sm" className="btn-group">
            <CButton
                color="secondary"
                variant="outline"
                href={item.detail_url}
                style={btnStyle}
                aria-label="detail"
                title="Detail"
            >
                <CIcon icon={cilSearch}/>
            </CButton>

            {item.edit_url && (
                <CButton
                    color="secondary"
                    variant="outline"
                    href={item.edit_url}
                    style={btnStyle}
                    aria-label="edit"
                    title="Edit"
                >
                    <CIcon icon={cilPencil}/>
                </CButton>
            )}

            {item.delete_url && (
                <CButton
                    color="secondary"
                    variant="outline"
                    href={item.delete_url}
                    style={btnStyle}
                    aria-label="delete"
                    title="Delete"
                >
                    <CIcon icon={cilTrash}/>
                </CButton>
            )}
        </CButtonGroup>
    );
}

function DataListView({listFields = [], fieldTypes = {}, items = [], isMultiSelect = false}) {
    return (
        <CTable bordered hover responsive size="sm">
            <CTableHead>
                <CTableRow>
                    {isMultiSelect && (
                        <CTableHeaderCell scope="col" style={{width: "40px"}}>
                            <CFormCheck checked={selectAll} onChange={handleSelectAll}/>
                        </CTableHeaderCell>
                    )}
                    <CTableHeaderCell scope="col" style={{width: "60px"}}>#</CTableHeaderCell>
                    {listFields.map((col) => (
                        <CTableHeaderCell key={`col_${col}`} scope="col">
                            {col}
                        </CTableHeaderCell>
                    ))}
                </CTableRow>
            </CTableHead>

            <CTableBody>
                {items.map((item, index) => (
                    <CTableRow key={`tb_row_${item.id ?? index}`}>
                        {isMultiSelect && (
                            <CTableDataCell key={`cb_${index}`} style={{verticalAlign: "middle", width: "40px"}}>
                                <CFormCheck
                                    checked={Boolean(selectedFlags[index])}
                                    onChange={() => handleSelectItem(index)}
                                />
                            </CTableDataCell>
                        )}

                        <CTableDataCell key={`tb_act_${index}`} scope="row"
                                        style={{verticalAlign: "middle", width: "60px"}}>
                            <ActionColumn item={item}/>
                        </CTableDataCell>

                        {listFields.map((field) => (
                            <CTableDataCell key={`${item.id ?? index}_${field}`}>
                                <ListViewHelper row_id={item.id ?? index} type={fieldTypes[field]} value={item[field]}/>
                            </CTableDataCell>
                        ))}
                    </CTableRow>
                ))}
            </CTableBody>
        </CTable>
    );
}

function Pagination({search_url, page = 1, page_size = 10, total = 0, keyword = null}) {
    const num_of_page = Math.max(1, Math.ceil(total / page_size));

    const buildUrl = (page_index) => {
        const params = new URLSearchParams();
        params.set("page", String(page_index));
        params.set("page_size", String(page_size));
        if (keyword !== null && String(keyword).trim() !== "" && keyword !== "null") {
            params.set("keyword", String(keyword));
        }
        return `${search_url}?${params.toString()}`;
    };

    const handlePrev = (e) => {
        e.preventDefault();
        if (page > 1) window.location.replace(buildUrl(page - 1));
    };

    const handleNext = (e) => {
        e.preventDefault();
        if (page < num_of_page) window.location.replace(buildUrl(page + 1));
    };

    const start = total === 0 ? 0 : (page - 1) * page_size + 1;
    const end = Math.min(page * page_size, total);

    return (
        <CButtonGroup role="group" aria-label="pagination">
            <CButton color="secondary" variant="outline" onClick={handlePrev} disabled={page <= 1}>
                &laquo;
            </CButton>

            <CButton color="secondary" variant="outline" disabled>
                {start} - {end} of {total}
            </CButton>

            <CButton color="secondary" variant="outline" onClick={handleNext} disabled={page >= num_of_page}>
                &raquo;
            </CButton>
        </CButtonGroup>
    );
}

function App({title, model}) {
    const data = JSON.parse(model);

    return (
        <CContainer fluid={true}>
            <CRow className="mb-3 align-items-center">
                <CCol>
                    <h4 className="m-0">{title}</h4>
                </CCol>
            </CRow>

            <CRow className="mb-3 g-2 align-items-center">
                <CCol md={8} lg={9}>
                    <SearchBox
                        search_url={data.search_url}
                        keyword={data.keyword}
                        page_size={data.page_size}
                    />
                </CCol>

                <CCol md={4} lg={3} className="text-end">
                    {data.add_url != null && <AddBox add_url={data.add_url}/>}
                </CCol>
            </CRow>

            <CRow>
                <CCol>
                    <CCard>
                        <CCardBody>
                            <DataListView
                                listFields={data["list_fields"]}
                                fieldTypes={data["field_types"]}
                                items={data["items"]}
                            />
                        </CCardBody>
                    </CCard>
                </CCol>
            </CRow>

            <CRow className="mt-3">
                <CCol md={6}></CCol>
                <CCol md={6} className="text-end">
                    <Pagination
                        search_url={data.search_url}
                        page={data.page}
                        page_size={data.page_size}
                        keyword={data.keyword}
                        total={data.total}
                    />
                </CCol>
            </CRow>
        </CContainer>
    );
}


const container = document.getElementById('root_container')
const root = createRoot(container)
const title = document.querySelector('meta[name="title"]').content
const model = document.querySelector('meta[name="model"]').content

root.render(
    <App title={title} model={model}/>
)
