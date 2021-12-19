function Output({data}) {

    if (JSON.stringify(data)===JSON.stringify({})) {
        return (
            <div>
                <h4>Please search for a company name</h4>
            </div>
        )
    }
    let headers = ['Company name', 'Website Url', 'Logo', 'Primarily used colors', 'Pie chart']
    let table_headers = headers.map( (header) =>  <th>{header}</th>)

    let no_of_colors = 2
    let primary_color_indices = data.counts_new.slice(0, no_of_colors).map(element => element[0])
    let primary_colors = []
    for (let i of primary_color_indices) {
        primary_colors.push(data.center_colors[i])
    }

    let column_values = primary_colors.map(primary_color => {
        let color = 'rgba('+parseInt(primary_color[0])+','+parseInt(primary_color[1])+','+parseInt(primary_color[2])+','+parseInt(primary_color[3])+')'
        return (
            <div>
                <span class='color-box' style={{backgroundColor:'rgba('+primary_color[0]+','+primary_color[1]+','+primary_color[2]+','+primary_color[3]+')'}}></span>
                <span>{color}</span>
            </div>
        )
    } )

    let table_data = []
    table_data.push(
        <tr>
            <td>{data.company_name}</td>
            <td><a href={data.website_url} target='blank'>Click Here</a></td>
            <td>
                <img src={data.website_logo} alt='Logo' class='logo' />
            </td>
            <td>
                <div class='flex-vertical'>
                    {column_values}
                </div>
            </td>
            <td>
                <img src={data.pie_chart_uri} alt='Pie Chart' class='pie-chart' />
            </td>
        </tr>
    )

    return (
        <div>
            <table>
                <thead>
                    <tr>
                        {table_headers}
                    </tr>
                </thead>
                <tbody>
                    {table_data}
                </tbody>
            </table>
        </div>
    )
}

export default Output