function create_listview_calendar(list)
{
    var i = 0
    calender_listmodel.clear()
    for (i = 0; i<list.length; i++){
        calender_listmodel.append({"name": list[i]})
    }
}

function create_listview_days_ahead(list)
{
    var i = 0
    days_listmodel.clear()
    for (i = 0; i<list.length; i++){
        days_listmodel.append({"name": list[i]})
    }
}
