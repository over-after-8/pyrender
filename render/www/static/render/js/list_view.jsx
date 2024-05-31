import {createRoot} from "react-dom/client";
import React, {useState} from "react";


function SearchBox({search_url, keyword, page_size}) {

    const [kw, setKw] = useState(keyword === "null" && "" || keyword)

    const search = () => {
        console.log(kw)

        const url = kw && `${search_url}?keyword=${kw}&page=${1}&page_size=${page_size}` || `${search_url}?page=${1}&page_size=${page_size}`
        window.location.replace(url)
    }

    return (
        <>
            <div className="row g-2">
                <div className="col-auto">
                    <input type="text" className="form-control" id="inputKeyword" value={kw}
                           onChange={(e) => setKw(e.target.value)}
                           placeholder="keyword..."/>
                </div>
                <div className="col-auto">
                    <button className="btn btn-primary mb-3" onClick={search}>Search</button>
                </div>
            </div>
        </>
    )
}

function AddBox({add_url}) {
    const add = () => {
        window.location.replace(add_url)
    }
    return (
        <>
            <button type="button" className="btn btn-info" onClick={add}>New</button>
        </>
    )
}


function ActionColumn({item}) {
    return (
        <>
            <div className={"btn-group"}>
                <a href={item.detail_url} className={"btn btn-sm btn-outline-secondary"}
                   style={{height: "25px", padding: "2px", width: "25px"}}>
                <span><i
                    className="bi bi-search"></i></span></a>
                <a className={"btn btn-sm btn-outline-secondary"} href={item.edit_url}
                   style={{height: "25px", padding: "2px", width: "25px"}}><span><i
                    className="bi bi-pencil"></i></span></a>
                <a className={"btn btn-sm btn-outline-secondary"} href={item.delete_url}
                   style={{height: "25px", padding: "2px", width: "25px"}}><span><i
                    className="bi bi-trash"></i></span></a>
            </div>
        </>
    )
}

function DataListView({listFields, fieldTypes, items}) {
    return (
        <>
            <table className="table table-bordered table-hover">
                <thead>
                <tr>
                    <th scope="col">#</th>
                    {listFields.map(x => {
                        return <th key={`col_${x}`} scope="col">{x}</th>
                    })}
                </tr>
                </thead>
                <tbody>

                {items.map((x, index) => {
                    return <tr key={`tb_row_${index}`}>
                        <td key={`tb_act_${index}`} scope={"row"}>
                            <ActionColumn item={x}></ActionColumn>
                        </td>
                        {listFields.map(c => <td key={`tb_col_${c}_${index}`}>{x[c]}</td>)}
                    </tr>
                })}
                </tbody>

            </table>
        </>
    )
}


function Pagination({search_url, page, page_size, total, keyword}) {

    const num_of_page = Math.ceil(total / page_size)

    const search = (page_index) => {
        const url = `${search_url}?keyword=${keyword}&page=${page_index}&page_size=${page_size}`
        console.log(url)
        window.location.replace(url)
    }

    const prev = () => {
        search(page - 1)
    }

    const next = () => {
        search(page + 1)
    }
    return (
        <>
            <nav aria-label="Page navigation example">
                <ul className="pagination">
                    {page > 1 &&
                        <li className="page-item">
                            <a className="page-link" href="#" aria-label="Previous" onClick={prev}>
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        </li>
                    }

                    <li className="page-item"><a className="page-link"
                                                 href="#">{(page - 1) * page_size + 1} - {Math.min(page * page_size, total)} of {total}</a>
                    </li>
                    {page < num_of_page &&
                        <li className="page-item">
                            <a className="page-link" href="#" aria-label="Next" onClick={next}>
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        </li>
                    }
                </ul>
            </nav>
        </>
    )
}


function App({title, model}) {
    const data = JSON.parse(model)
    console.log(data)
    return (
        <>
            <h2>{title}</h2>
            <div className={"mt-3 row"}>
                <div className={"col-10"}>
                    <SearchBox search_url={data.search_url} keyword={data.keyword}
                               page_size={data.page_size}></SearchBox>
                </div>
                <div className={"col-2 text-end"}>
                    <AddBox add_url={data.add_url}></AddBox>
                </div>
            </div>
            <div className={"mt-1"}>
                <DataListView listFields={data["list_fields"]} fieldTypes={data["field_types"]}
                              items={data["items"]}></DataListView>
                <Pagination search_url={data.search_url} page={data.page} page_size={data.page_size}
                            keyword={data.keyword} total={data.total}></Pagination>
            </div>
        </>
    )
}


const container = document.getElementById('root_container')
const root = createRoot(container)
const title = document.querySelector('meta[name="title"]').content
const model = document.querySelector('meta[name="model"]').content

root.render(
    <App title={title} model={model}/>
)
