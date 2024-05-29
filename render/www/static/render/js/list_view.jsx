import {createRoot} from "react-dom/client";
import React from "react";


function SearchBox({model}) {
    return (
        <>
            <form className="row g-2" method={"GET"}>
                <div className="col-auto">
                    <input type="text" className="form-control" id="inputKeyword" placeholder="keyword..."/>
                </div>
                <div className="col-auto">
                    <button className="btn btn-primary mb-3">Search</button>
                </div>
            </form>
        </>
    )
}

function AddBox({model}) {
    return (
        <>
            <button type="button" className="btn btn-info">New</button>
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

                {items.map(x => {
                    return <tr>
                        <td scope={"row"}></td>
                        {listFields.map(c => <td>{x[c]}</td>)}
                    </tr>
                })}
                </tbody>

            </table>
        </>
    )
}

function Pagination({model}) {
    return (
        <>
            <nav aria-label="Page navigation example">
                <ul className="pagination">
                    <li className="page-item">
                        <a className="page-link" href="#" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    <li className="page-item"><a className="page-link" href="#">1 - 20 of 100</a></li>
                    <li className="page-item">
                        <a className="page-link" href="#" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                </ul>
            </nav>
        </>
    )
}


function App({title, model}) {
    const data = JSON.parse(model)
    return (
        <>
            <h2>{title}</h2>
            <div className={"mt-3 row"}>
                <div className={"col-10"}>
                    <SearchBox></SearchBox>
                </div>
                <div className={"col-2 text-end"}>
                    <AddBox></AddBox>
                </div>
            </div>
            <div className={"mt-1"}>
                <DataListView listFields={data["list_fields"]} fieldTypes={data["field_types"]}
                              items={data["items"]}></DataListView>
                <Pagination></Pagination>
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
