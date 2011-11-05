function createListView(list)
{
    var i = 0;
    calender_listmodel.clear()
    for (i=0; i<list.length; i++){
        calender_listmodel.append({"name": list[i]})
    }
}
