import {createRoot} from "react-dom/client";
import React, {useState} from "react";


function ListViewHelper({value, type, row_id}) {

  switch (type) {
    case "Boolean":
      return (
        <input className="form-check-input" disabled type="checkbox" checked={value}></input>
      )
    case "Relationship":
      if (typeof value === "string") {
        return (
          <span className={"badge text-bg-secondary me-1"}>{value}</span>
        )
      } else {
        return (
          <>
            {
              value.map((item) => {
                return <span className={"badge text-bg-secondary me-1"}
                             key={`${row_id}_${item}`}>{item}</span>
              })
            }
          </>
        )
      }
    case "JobRunStatus":
      return <span className="badge text-bg-secondary me-2">{value}</span>
    default:
      return (
        <span>{value}</span>
      )
  }
}


function SearchBox({search_url, keyword, page_size}) {

  let kkw = ""
  if (keyword === "null" || keyword === null) {
    kkw = ""
  } else {
    kkw = keyword
  }

  const [kw, setKw] = useState(kkw)

  const search = () => {

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
      <button type="button" className="btn btn-outline-success" onClick={add}>New</button>
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
        {
          item.edit_url && <a className={"btn btn-sm btn-outline-secondary"} href={item.edit_url}
                              style={{height: "25px", padding: "2px", width: "25px"}}><span><i
            className="bi bi-pencil"></i></span></a>
        }
        {
          item.delete_url && <a className={"btn btn-sm btn-outline-secondary"} href={item.delete_url}
                                style={{height: "25px", padding: "2px", width: "25px"}}><span><i
            className="bi bi-trash"></i></span></a>
        }

      </div>
    </>
  )
}

function DataListView({listFields, fieldTypes, items, isMultiSelect}) {


  const selectValues = new Map()
  const setSelectValues = new Map()


  const [selectAll, setSelectAll] = useState(false)

  items.forEach((x, index) => {
    const [selectValue, setSelectValue] = useState(false)

    selectValues[index] = selectValue
    setSelectValues[index] = setSelectValue
  })

  const selectAllOnChange = () => {
    const isSelect = !selectAll
    setSelectAll(!selectAll)

    items.forEach((x, index) => {
      setSelectValues[index](isSelect)
    })
  }

  const selectItem = (index) => {
    let all = true
    items.forEach((x, idx) => {
      if (idx === index) {
        all = all && !selectValues[idx]
      } else {
        all = all && selectValues[idx]
      }

    })
    setSelectAll(all)
    setSelectValues[index](!selectValues[index])
    console.log(selectValues)
  }

  return (
    <>
      <table className="table table-bordered table-hover table-sm">
        <thead>
        <tr>
          {
            isMultiSelect && <th scope={"col"}>
              <input type={"checkbox"} className={"form-check-input"} checked={selectAll}
                     onChange={() => selectAllOnChange()}></input>
            </th>
          }

          <th scope="col">#</th>
          {listFields.map(x => {
            return <th key={`col_${x}`} scope="col">{x}</th>
          })}
        </tr>
        </thead>
        <tbody>
        {items.map((x, index) => {
          return <tr key={`tb_row_${index}`}>
            {
              isMultiSelect && <td scope={"col"} key={`cb_${index}`}>
                <input className={"form-check-input"} type={"checkbox"} checked={selectValues[index]}
                       value={selectValues[index] && 1 || 0}
                       onChange={() => selectItem(index)}></input>
              </td>
            }
            <td key={`tb_act_${index}`} scope={"row"}>
              <ActionColumn item={x}></ActionColumn>
            </td>
            {
              listFields.map((field) => {
                return <td key={`${x.id}_${field}`}><ListViewHelper key={`f_${x.id}_${field}`}
                                                                    row_id={x.id}
                                                                    type={fieldTypes[field]}
                                                                    value={x[field]}></ListViewHelper>
                </td>
              })
            }
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
    let url = `${search_url}?page=${page_index}&page_size=${page_size}`
    if (keyword !== null) {
      url = `${url}&keyword=${keyword}`
    }

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


function ActionMultiSelect({actions}) {
  return (
    <>
      <div className="dropdown">
        <button className="btn btn-outline-success dropdown-toggle" type="button" data-bs-toggle="dropdown"
                aria-expanded="false">
          Actions
        </button>
        <ul className="dropdown-menu">
          {
            Object.keys(actions).map((x, index) => {
              return <li key={`action_${index}`}><a className="dropdown-item" href={actions[x]}>{x}</a></li>
            })
          }
        </ul>
      </div>
    </>
  )
}


function App({title, model}) {
  const data = JSON.parse(model)
  const isMultiSelect = Object.keys(data["multi_select_actions"]).length > 0
  return (
    <>
      <h2>{title}</h2>
      <div className={"mt-3 row"}>
        <div className={"col-10"}>
          <SearchBox search_url={data.search_url} keyword={data.keyword}
                     page_size={data.page_size}></SearchBox>
        </div>
        <div className={"col-2 text-end"}>
          {
            data.add_url != null && <AddBox add_url={data.add_url}></AddBox>
          }

        </div>
      </div>
      <div className={"mt-1"}>
        <div className={"row"}>
          <div className={"col col-md-6"}>
            {
              isMultiSelect && <div className={"float-start"}>
                <ActionMultiSelect actions={data["multi_select_actions"]}></ActionMultiSelect>
              </div>
            }

          </div>
          <div className={"col col-md-6"}>
            <div className={"float-end"}>
              <Pagination search_url={data.search_url} page={data.page} page_size={data.page_size}
                          keyword={data.keyword} total={data.total}></Pagination>
            </div>
          </div>
        </div>

        <div>
          <DataListView listFields={data["list_fields"]} fieldTypes={data["field_types"]}
                        items={data["items"]}
                        isMultiSelect={isMultiSelect}></DataListView>
        </div>
        <div className={"row"}>
          <div className={"col col-md-6"}></div>
          <div className={"col col-md-6"}>
            <div className={"float-end"}>
              <Pagination search_url={data.search_url} page={data.page} page_size={data.page_size}
                          keyword={data.keyword} total={data.total}></Pagination>
            </div>
          </div>
        </div>


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
