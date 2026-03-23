class Application {
    constructor(name, url, menu) {
        this.name = name
        this.url = url
    }
}

function createApplications(jsonData) {
    return jsonData.map(appObj => {
        const menuObj = appObj.menu
        return new Application(appObj.name, appObj.url)
    });
}

export default createApplications