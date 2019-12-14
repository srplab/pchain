function findFromProc(proc, objectid) {
    if (proc["ObjectID"] && proc["ObjectID"] == objectid)
        return proc;
    if (proc["InputQueue"]) {
        var input = proc["InputQueue"];
        for (var i = 0; i < input.length; i++) {
            if (input[i]["ObjectID"] && input[i]["ObjectID"] == objectid)
                return input[i];
        }
    }
    if (proc["OutputQueue"]) {
        var output = proc["OutputQueue"];
        for (var i = 0; i < output.length; i++) {
            var output_set = output[i];
            if (output_set["ObjectID"] && output_set["ObjectID"] == objectid)
                return output_set;
            if (output_set.PCData) {
                for (var j = 0; j < output_set.PCData.length; j++) {
                    if (output_set.PCData[j]["ObjectID"] && output_set.PCData[j]["ObjectID"] == objectid)
                        return output_set.PCData[j];
                }
            }
        }
    }
    if (proc["PCProcChild"]) {
        var child = proc["PCProcChild"];
        for (var i = 0; i < child.length; i++) {
            for (var j = 0; j < child[i].length; j++) {
                var result = findFromProc(child[i][j], objectid);
                if (result)
                    return result;
            }
        }
    }
    return undefined;
}
function findFromRunner(runner, objectid) {
    if (runner["ObjectID"] && runner["ObjectID"] == objectid)
        return runner;
    var proc = runner["PCProcStart"];
    for (var i = 0; i < proc.length; i++) {
        var result = findFromProc(proc[i], objectid);
        if (result)
            return result;
    }
    return undefined;
}
function findFromObjectList(objectlist, objectid) {
    if (ObjectIDTable[objectid])
        return ObjectIDTable[objectid];
    for (var m = 0; m < objectlist.length; m++) {
        if (objectlist[m]["ObjectID"] && objectlist[m]["ObjectID"] == objectid) {
            ObjectIDTable[objectid] = objectlist[m];
            return objectlist[m];
        }
        if (objectlist[m]["EnvDataQueue"]) {
            var data = objectlist[m]["EnvDataQueue"];
            for (var i = 0; i < data.length; i++) {
                if (data[i]["ObjectID"] && data[i]["ObjectID"] == objectid) {
                    ObjectIDTable[objectid] = data[i];
                    return data[i];
                }
            }
        }
        if (objectlist[m]["NormalRunnerQueue"]) {
            var runner = objectlist[m]["NormalRunnerQueue"];
            for (var i = 0; i < runner.length; i++) {
                var result = findFromRunner(runner[i], objectid);
                if (result) {
                    ObjectIDTable[objectid] = result;
                    return result;
                }
            }
        }
    }
    return undefined;
}
function elementFromObjectList(objectlist, objectid) {
    if (ElementIDTable[objectid])
        return ElementIDTable[objectid];
    for (var m = 0; m < objectlist.length; m++) {
        if (objectlist[m]["Elements"]) {
            var data = objectlist[m]["Elements"];
            for (var i = 0; i < data.length; i++) {
                if (data[i]["ObjectID"] && data[i]["ObjectID"] == objectid) {
                    ElementIDTable[objectid] = data[i];
                    return data[i];
                }
            }
        }
        if (objectlist[m]["NormalRunnerQueue"]) {
            var runner = objectlist[m]["NormalRunnerQueue"];
            for (var i = 0; i < runner.length; i++) {
                if (runner[i]["Elements"]) {
                    var runner_item = runner[i]["Elements"];
                    for (var j = 0; j < runner_item.length; j++) {
                        if (runner_item[j]["ObjectID"] && runner_item[j]["ObjectID"] == objectid) {
                            ElementIDTable[objectid] = runner_item[j];
                            return runner_item[j];
                        }
                    }
                }
            }
        }
    }
    return undefined;
}
var RenderJSonData = undefined;
var RenderProcWidth = 0;
var RenderProcHeight = 0;
var RenderDataRadius = 0;
var RenderHInterval = 0;
var RenderVInterval = 0;
var ObjectIDTable = [];
var ElementIDTable = [];
var RenderSvgWidth = 0;
var RenderSvgHeight = 0;
var EnvData_Stroke = "#339933";
var EnvData_Fill = "#ffffff";
var TipWindow_Stroke = "#000000";
var TipWindow_Fill = "#FFFFFF";
var TipWindow_Text_Stroke = "#000000";
var ElementInput_Stroke = "#339933";
var ElementInput_Fill = "#ffffff";
var ElementInput_Text_Stroke = "#000000";
var ElementData_Stroke = "#339933";
var ElementData_Fill = "#ffffff";
var ElementProc_Stroke = "#339933";
var ElementProc_Fill = "#ffffff";
var ElementProc_Fill_Current = "#ffcccc";
var ElementProc_Text_Stroke = "#000000";
var ProcInternalLine_Stroke = "#339933";
var ProcOutSideLine_Stroke = "#cccccc";
var DataLine_Stroke = "#0000FF";
var RenderProcStack; /*--hold pccell object, each item is {"objectid":xxx,"objectname":xxx} */
function render_request(url) {
    try {
        d3.json(url, function (indata) {
            //d3.json(url, { "cache": "no-cache" }).then(function (err,indata) {
            if (indata == null) {
                if (url.indexOf('/realm/cellstatus') == 0 || url.indexOf('/realm/cellrunonce') == 0) {
                    RenderProcStack = [];
                    render_request("/realm/status");
                }
            }
            render_realm(indata);
        });
    }
    catch (error) {
        alert(error);
    }
}
function render_realm(indata) {
    if (!indata)
        return;
    RenderJSonData = indata;
    RenderProcWidth = indata.ProcWidth;
    RenderProcHeight = indata.ProcHeight;
    RenderDataRadius = indata.DataRadius;
    RenderHInterval = indata.HInterval;
    RenderVInterval = indata.VInterval;
    ObjectIDTable = [];
    ElementIDTable = [];
    var svgwidth = 0;
    var svgHeight = 0;
    var pccell = [];
    var ObjectList = indata["ObjectList"];
    for (var i = 0; i < ObjectList.length; i++) {
        pccell.push(ObjectList[i].ObjectID);
        if (ObjectList[i].NormalRunnerQueue) {
            for (var j = 0; j < ObjectList[i].NormalRunnerQueue.length; j++) {
                var runner = ObjectList[i].NormalRunnerQueue[j];
                if (runner.Width && runner.Width > svgwidth)
                    svgwidth = runner.Width;
            }
            svgHeight = svgHeight + ObjectList[i].NormalRunnerQueue[ObjectList[i].NormalRunnerQueue.length - 1].PosY + ObjectList[i].NormalRunnerQueue[ObjectList[i].NormalRunnerQueue.length - 1].Height;
        }
    }
    RenderSvgWidth = svgwidth;
    RenderSvgHeight = svgHeight;
    render_pccell(ObjectList, pccell, svgwidth, svgHeight);
}
function render_resize() {
    if (RenderJSonData) {
        var svgwidth = 0;
        var svgHeight = 0;
        var ObjectList = RenderJSonData["ObjectList"];
        for (var i = 0; i < ObjectList.length; i++) {
            if (ObjectList[i].NormalRunnerQueue) {
                for (var j = 0; j < ObjectList[i].NormalRunnerQueue.length; j++) {
                    var runner = ObjectList[i].NormalRunnerQueue[j];
                    if (runner.Width && runner.Width > svgwidth)
                        svgwidth = runner.Width;
                }
                svgHeight = svgHeight + ObjectList[i].NormalRunnerQueue[ObjectList[i].NormalRunnerQueue.length - 1].PosY + ObjectList[i].NormalRunnerQueue[ObjectList[i].NormalRunnerQueue.length - 1].Height;
            }
        }
        var cell = d3.select("body").selectAll("div#" + "cell");
        if (document.body.clientWidth < svgwidth) {
            cell.select("svg").attr("style", "border:1px solid #000000")
                .attr("width", '100%')
                .attr("height", svgHeight * document.body.clientWidth / svgwidth)
                .attr('viewBox', '0,0,' + svgwidth + ',' + svgHeight);
        }
        else {
            cell.select("svg").attr("style", "border:1px solid #000000")
                .attr("width", '100%')
                .attr("height", svgHeight)
                .attr('viewBox', '0,0,' + document.body.clientWidth + ',' + svgHeight);
        }
    }
}
/*-----------render pccell---------------------------------*/
function render_pccell(ObjectList, dataset, svgwidth, svgHeight) {
    d3.select("body").selectAll("div#" + "cell").remove();
    d3.select("body").selectAll("div#" + "cell")
        .data(dataset)
        .enter()
        .append("div")
        .attr("margin", "0em")
        .attr("id", "cell")
        .append("div")
        .attr("height", "100")
        .each(function (d) {
        var cell_div = d3.select(this.parentNode);
        var svg = cell_div.append("svg");
        var defs = svg.append("defs");
        var arrowMarker = defs.append("marker")
            .attr("id", "linearrow")
            .attr("markerUnits", "strokeWidth")
            .attr("markerWidth", "8")
            .attr("markerHeight", "8")
            .attr("viewBox", "0 0 12 12")
            .attr("refX", "13")
            .attr("refY", "6")
            .attr("orient", "auto");
        var arrow_path = "M0,0 L12,6 L0,12 L6,6 L0,0";
        arrowMarker.append("path").attr("d", arrow_path).attr("fill", "#0000FF");
    });
    d3.select("body").selectAll("div#" + "cell")
        .data(dataset)
        .each(function (d) {
        var cell = findFromObjectList(ObjectList, d);
        /*--each cell--*/
        var cell_div = d3.select(this).select("div").attr("style", "position:relative;margin-bottom:10px");
        var text_div = cell_div.append("div")
            .attr("style", "left:0;width:49%");
        var button_div = cell_div.append("div")
            .attr("style", "width:49%;left:50%;position:absolute;bottom:0;");
        button_div.append("button")
            .text("Next Step")
            .on("click", function (d) {
            if (USEEMBEDFILE)
                render_request("/pcstatus.json");
            else {
                if (RenderProcStack.length == 0)
                    render_request("/realm/runonce");
                else
                    render_request("/realm/cellrunonce/" + RenderProcStack[RenderProcStack.length - 1].objectid);
            }
        });
        var ParentCellButton = button_div.append("button")
            .text("Parent Cell")
            .attr("disabled", "false")
            .attr("style", "margin-left:20px")
            .on("click", function (d) {
            if (USEEMBEDFILE)
                return;
            else {
                if (RenderProcStack.length == 0)
                    return;
                RenderProcStack.pop();
                if (RenderProcStack.length == 0)
                    render_request("/realm/status");
                else
                    render_request("/realm/cellstatus/" + RenderProcStack[RenderProcStack.length - 1].objectid);
            }
        });
        if (cell.ParentCell)
            ParentCellButton.attr('disabled', null);
        text_div.append("h3").text(cell.ObjectName);
        var cell_txt = "";
        if (cell.IsSuspend == true)
            cell_txt = cell_txt + "IsSuspend : true";
        else
            cell_txt = cell_txt + "IsSuspend : false";
        if (cell.IsOutputGenerated == true)
            cell_txt = cell_txt + "      IsOutputGenerated : true";
        else
            cell_txt = cell_txt + "      IsOutputGenerated : false";
        cell_txt = cell_txt + "      Status : " + cell.Status;
        cell_txt = cell_txt + "      NextRunTick : " + cell.NextRunTick;
        if (cell.IsReady == true)
            cell_txt = cell_txt + "      IsReady : true";
        else
            cell_txt = cell_txt + "      IsReady : false";
        cell_txt = cell_txt + "      RunningStatus : " + cell.RunningStatus;
        text_div.append("text").text(cell_txt);
        var svg = d3.select(this).select("svg");
        if (document.body.clientWidth < svgwidth) {
            svg.attr("style", "border:1px solid #000000")
                .attr("width", '100%')
                .attr("height", svgHeight * document.body.clientWidth / svgwidth)
                .attr('viewBox', '0,0,' + svgwidth + ',' + svgHeight);
        }
        else {
            svg.attr("style", "border:1px solid #000000")
                .attr("width", '100%')
                .attr("height", svgHeight)
                .attr('viewBox', '0,0,' + document.body.clientWidth + ',' + svgHeight);
        }
        if (cell.Elements) {
            svg.selectAll("g#EnvData").remove();
            svg.selectAll("g#EnvData")
                .data(cell.Elements)
                .enter()
                .append("g")
                .attr("id", "EnvData")
                .append("circle")
                .attr("cx", function (d) { return d.PosX; })
                .attr("cy", function (d) { return d.PosY; })
                .attr("r", function (d) { return d.Radius; })
                .attr("stroke", EnvData_Stroke)
                .attr("fill", EnvData_Fill)
                .on("mouseover", function (d, i) {
                var rect = d3.select(this);
                if (!proc_item_timer) {
                    proc_item_timer = setTimeout(function (d) {
                        //rect.attr("fill", "#FF0000 ");
                        var w_PosX = d.PosX - 200 / 2;
                        var w_PosY = d.PosY - 60;
                        if (w_PosY < 0) {
                            w_PosX = d.PosX + d.Radius + 10;
                            w_PosY = 10;
                        }
                        if (w_PosX < 0) {
                            w_PosX = 10;
                        }
                        var w_Width = 200;
                        var w_Height = 40;
                        var w_svg = svg.append("g")
                            .attr("id", "FloatWindow");
                        w_svg.append("rect")
                            .attr("x", w_PosX).attr("y", w_PosY).attr("width", w_Width).attr("height", w_Height)
                            .attr("stroke", TipWindow_Stroke).attr("fill", TipWindow_Fill);
                        var data_def = findFromObjectList(ObjectList, d.ObjectID);
                        var text_ele = w_svg.append("text")
                            .attr("x", function (d) { return w_PosX; })
                            .attr("y", function (d) { return w_PosY; })
                            .attr("fill", TipWindow_Text_Stroke)
                            .attr("font-size", "14");
                        text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 20).text(data_def.ObjectName.substring(0, 20));
                    }, 500, d);
                }
            })
                .on("mouseout", function (d, i) {
                clearTimeout(proc_item_timer);
                proc_item_timer = null;
                svg.selectAll("g#FloatWindow").remove();
            });
            var EnvData_text_item = svg.selectAll("g#EnvData");
            EnvData_text_item.append("text")
                .attr("x", function (d) { return d.PosX; })
                .attr("y", function (d) { return d.PosY; })
                .attr("fill", ElementInput_Text_Stroke)
                .attr("font-size", "8")
                .attr("dx", function (d) {
                var EnvData_def = findFromObjectList(ObjectList, d.ObjectID);
                var num = 1;
                var tick = parseInt(EnvData_def.ScheduleTickCount);
                while ((tick / 10) >= 1) {
                    tick = tick / 10;
                    num = num + 1;
                }
                return -0.3 * num + "em";
            })
                .attr("dy", "0.3em")
                .attr("style", "pointer-events: none;")
                .text(function (d, i) {
                var EnvData_def = findFromObjectList(ObjectList, d.ObjectID);
                return EnvData_def.ScheduleTickCount;
            });
        }
        if (cell.NormalRunnerQueue) {
            var runner = [];
            for (var i = 0; i < cell.NormalRunnerQueue.length; i++) {
                runner.push(cell.NormalRunnerQueue[i].ObjectID);
            }
            render_runner(ObjectList, runner, svg);
        }
    });
}
function render_runner(ObjectList, dataset, svg) {
    svg.selectAll("g#NormalRunnerQueue")
        .data(dataset)
        .enter()
        .append("g")
        .attr("id", "NormalRunnerQueue")
        .each(function (d) {
        render_runner_each(ObjectList, d3.select(this), d, svg);
    });
}
var proc_item_timer;
function render_runner_each(ObjectList, svg, id, host) {
    var runner = findFromObjectList(ObjectList, id);
    svg.append("text")
        .attr("x", runner.PosX + RenderDataRadius)
        .attr("y", runner.PosY + RenderDataRadius)
        .attr("fill", ElementInput_Text_Stroke)
        .attr("font-size", "14")
        .attr("dx", "-0.3em")
        .attr("dy", "0.3em")
        .attr("style", "pointer-events: none;")
        .text(runner.ObjectName);
    if (runner.Elements) {
        var item = svg.selectAll("g#nodes")
            .data(runner.Elements)
            .enter()
            .append("g")
            .attr("id", "nodes")
            .attr("class", function (d) {
            return d.Type;
        });
        var input_item = svg.selectAll(".ElementInput");
        input_item.append("circle")
            .attr("cx", function (d) { return d.PosX; })
            .attr("cy", function (d) { return d.PosY; })
            .attr("r", function (d) {
            return d.Radius;
        })
            .attr("stroke", ElementInput_Stroke)
            .attr("fill", ElementInput_Fill)
            .on("mouseover", function (d, i) {
            var rect = d3.select(this);
            if (!proc_item_timer) {
                proc_item_timer = setTimeout(function (d) {
                    //rect.attr("fill", "#FF0000 ");
                    var w_PosX = d.PosX - 200 / 2;
                    var w_PosY = d.PosY - 100;
                    if (w_PosY < 0) {
                        w_PosX = d.PosX + d.Radius + 10;
                        w_PosY = 10;
                    }
                    if (w_PosX < 0) {
                        w_PosX = 10;
                    }
                    var w_Width = 200;
                    var w_Height = 80;
                    var w_svg = host.append("g")
                        .attr("id", "FloatWindow");
                    w_svg.append("rect").attr("x", w_PosX).attr("y", w_PosY).attr("width", w_Width).attr("height", w_Height)
                        .attr("stroke", TipWindow_Stroke).attr("fill", TipWindow_Fill);
                    var input_def = findFromObjectList(ObjectList, d.ObjectID);
                    var text_ele = w_svg.append("text")
                        .attr("x", function (d) { return w_PosX; })
                        .attr("y", function (d) { return w_PosY; })
                        .attr("fill", TipWindow_Text_Stroke)
                        .attr("font-size", "14");
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 20).text(input_def.DataBaseName.substring(0, 20));
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 40).text("RequestNumber : " + input_def.RequestNumber);
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 60).text("IsFromInternal : " + input_def.IsFromInternal);
                }, 500, d);
            }
        })
            .on("mouseout", function (d, i) {
            clearTimeout(proc_item_timer);
            proc_item_timer = null;
            host.selectAll("g#FloatWindow").remove();
        });
        var input_text_item = svg.selectAll(".ElementInput");
        input_text_item.append("text")
            .attr("x", function (d) { return d.PosX; })
            .attr("y", function (d) { return d.PosY; })
            .attr("fill", ElementInput_Text_Stroke)
            .attr("font-size", "12")
            .attr("dx", "-0.3em")
            .attr("dy", "0.3em")
            .attr("style", "pointer-events: none;")
            .text(function (d, i) {
            var input_def = findFromObjectList(ObjectList, d.ObjectID);
            return input_def.RequestNumber;
        });
        var output_item = svg.selectAll(".ElementOutput");
        output_item.append("rect")
            .attr("x", function (d) {
            return d.PosX;
        })
            .attr("y", function (d) {
            return d.PosY;
        })
            .attr("width", function (d) {
            return d.Width;
        })
            .attr("height", function (d) {
            return d.Width;
        })
            .attr("stroke", "#339933")
            .attr("fill", "#ffffff")
            .on("mouseover", function (d, i) {
            var rect = d3.select(this);
            if (!proc_item_timer) {
                proc_item_timer = setTimeout(function (d) {
                    var w_PosX = d.PosX - (200 - RenderDataRadius) / 2;
                    var w_PosY = d.PosY - 60;
                    if (w_PosY < 0) {
                        w_PosX = d.PosX + d.Radius + 10;
                        w_PosY = 10;
                    }
                    if (w_PosX < 0) {
                        w_PosX = 10;
                    }
                    var w_Width = 200;
                    var w_Height = 40;
                    var w_svg = host.append("g")
                        .attr("id", "FloatWindow");
                    w_svg.append("rect").attr("x", w_PosX).attr("y", w_PosY).attr("width", w_Width).attr("height", w_Height)
                        .attr("stroke", TipWindow_Stroke).attr("fill", TipWindow_Fill);
                    var output_def = findFromObjectList(ObjectList, d.ObjectID);
                    var text_ele = w_svg.append("text")
                        .attr("x", function (d) { return w_PosX; })
                        .attr("y", function (d) { return w_PosY; })
                        .attr("fill", TipWindow_Text_Stroke)
                        .attr("font-size", "14");
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 20).text(output_def.DataBaseName.substring(0, 20));
                }, 500, d);
            }
        })
            .on("mouseout", function (d, i) {
            clearTimeout(proc_item_timer);
            proc_item_timer = null;
            //var rect = d3.select(this);
            //rect.attr("fill", "#ffffff ");
            host.selectAll("g#FloatWindow").remove();
        });
        var data_item = svg.selectAll(".ElementData");
        data_item.append("circle")
            .attr("cx", function (d) { return d.PosX; })
            .attr("cy", function (d) { return d.PosY; })
            .attr("r", function (d) {
            return d.Radius;
        })
            .attr("stroke", ElementData_Stroke)
            .attr("fill", ElementData_Fill)
            .on("mouseover", function (d, i) {
            var rect = d3.select(this);
            if (!proc_item_timer) {
                proc_item_timer = setTimeout(function (d) {
                    //rect.attr("fill", "#FF0000 ");
                    var w_PosX = d.PosX - 200 / 2;
                    var w_PosY = d.PosY - 60;
                    if (w_PosY < 0) {
                        w_PosX = d.PosX + d.Radius + 10;
                        w_PosY = 10;
                    }
                    if (w_PosX < 0) {
                        w_PosX = 10;
                    }
                    var w_Width = 200;
                    var w_Height = 40;
                    var w_svg = host.append("g")
                        .attr("id", "FloatWindow");
                    w_svg.append("rect").attr("x", w_PosX).attr("y", w_PosY).attr("width", w_Width).attr("height", w_Height)
                        .attr("stroke", TipWindow_Stroke).attr("fill", TipWindow_Fill);
                    var data_def = findFromObjectList(ObjectList, d.ObjectID);
                    var text_ele = w_svg.append("text")
                        .attr("x", function (d) { return w_PosX; })
                        .attr("y", function (d) { return w_PosY; })
                        .attr("fill", TipWindow_Text_Stroke)
                        .attr("font-size", "14");
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 20).text(data_def.ObjectName.substring(0, 20));
                }, 500, d);
            }
        })
            .on("mouseout", function (d, i) {
            clearTimeout(proc_item_timer);
            proc_item_timer = null;
            host.selectAll("g#FloatWindow").remove();
        });
        var proc_item = svg.selectAll(".ElementProc");
        proc_item.append("rect")
            .attr("x", function (d) {
            return d.PosX;
        })
            .attr("y", function (d) {
            return d.PosY;
        })
            .attr("width", function (d) {
            return d.Width;
        })
            .attr("height", function (d) {
            return d.Height;
        })
            .attr("stroke", ElementProc_Stroke)
            .on("mouseover", function (d, i) {
            var rect = d3.select(this);
            if (!proc_item_timer) {
                proc_item_timer = setTimeout(function (d) {
                    //rect.attr("fill", "#FF0000 ");
                    var w_PosX = d.PosX - (200 - RenderProcWidth) / 2;
                    var w_PosY = d.PosY - 160;
                    var w_Width = 200;
                    var w_Height = 140;
                    if (w_PosY < 0) {
                        w_PosX = d.PosX + RenderProcWidth + 10;
                        w_PosY = 10;
                        if (w_PosX < 0) {
                            w_PosX = 10;
                        }
                        else if (w_PosX + w_Width > RenderSvgWidth) {
                            w_PosX = d.PosX - w_Width - 10;
                        }
                    }
                    else {
                        if (w_PosX < 0) {
                            w_PosX = 10;
                        }
                        else if (w_PosX + w_Width > RenderSvgWidth) {
                            w_PosX = RenderSvgWidth - w_Width - 10;
                        }
                    }
                    var w_svg = host.append("g")
                        .attr("id", "FloatWindow");
                    w_svg.append("rect").attr("x", w_PosX).attr("y", w_PosY).attr("width", w_Width).attr("height", w_Height)
                        .attr("stroke", TipWindow_Stroke).attr("fill", TipWindow_Fill);
                    var proc_def = findFromObjectList(ObjectList, d.ObjectID);
                    var text_ele = w_svg.append("text")
                        .attr("x", function (d) { return w_PosX; })
                        .attr("y", function (d) { return w_PosY; })
                        .attr("fill", TipWindow_Text_Stroke)
                        .attr("font-size", "14");
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 20).text(proc_def.ObjectName.substring(0, 20));
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 40).text("IsSuspend : " + proc_def.IsSuspend);
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 60).text("IsOutputGenerated : " + proc_def.IsOutputGenerated);
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 80).text("ChildEndMarker : " + proc_def.ChildEndMarker);
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 100).text("Status : " + proc_def.Status);
                    text_ele.append("tspan").attr("x", w_PosX + 10).attr("y", w_PosY + 120).text("NextRunTick : " + proc_def.NextRunTick);
                }, 500, d);
            }
        })
            .on("mouseout", function (d, i) {
            clearTimeout(proc_item_timer);
            proc_item_timer = null;
            //var rect = d3.select(this);
            //rect.attr("fill", "#ffffff ");
            host.selectAll("g#FloatWindow").remove();
        })
            .on("click", function (d, i) {
            if (USEEMBEDFILE)
                render_request("/pcstatus.json");
            else {
                var proc_def = findFromObjectList(ObjectList, d.ObjectID);
                if (proc_def.Type == "PCCell") {
                    RenderProcStack = []; /*--hold pccell object, each item is {"objectid":xxx,"objectname":xxx} */
                    RenderProcStack.push({
                        "objectid": d.ObjectID, "objectname": d.ObjectName
                    });
                    render_request("/realm/cellstatus/" + d.ObjectID);
                }
            }
        })
            .each(function (d) {
            var proc_ele = d3.select(this);
            var proc_def = findFromObjectList(ObjectList, d.ObjectID);
            if (proc_def.IsCurrent && proc_def.IsCurrent == true) {
                proc_ele.attr("fill", ElementProc_Fill_Current);
            }
            else {
                proc_ele.attr("fill", ElementProc_Fill);
            }
        });
        var proc_text_item = svg.selectAll(".ElementProc");
        proc_text_item.append("text")
            .attr("x", function (d) { return d.PosX; })
            .attr("y", function (d) { return d.PosY + d.Height / 2; })
            .attr("dx", "0.3em")
            .attr("dy", "0.3em")
            .attr("fill", ElementProc_Text_Stroke)
            .attr("font-size", "12")
            .text(function (d, i) {
            var proc_def = findFromObjectList(ObjectList, d.ObjectID);
            return proc_def.ObjectName.substring(0, 12);
        });
    }
    /*--render line in proc--*/
    var links = [];
    var proclinks = [];
    if (runner.PCProcStart) {
        var prev_proc_item = null;
        for (var i = 0; i < runner.PCProcStart.length; i++) {
            var procs = runner.PCProcStart[i];
            var child_links = render_runner_collectline(ObjectList, procs);
            links = links.concat(child_links);
            /*---lines between procs--*/
            child_links = render_runner_collectpoints(ObjectList, procs);
            proclinks = proclinks.concat(child_links);
            var child_proc_item = elementFromObjectList(ObjectList, procs.ObjectID);
            if (prev_proc_item) {
                child_links = render_runner_connectpoint(ObjectList, prev_proc_item.PosX + prev_proc_item.Width, prev_proc_item.PosY + prev_proc_item.Height / 2, child_proc_item.PosX, child_proc_item.PosY + child_proc_item.Height / 2);
                proclinks = proclinks.concat(child_links);
            }
            prev_proc_item = child_proc_item;
        }
    }
    if (links.length != 0) {
        var item = svg.selectAll("g#procinternalline")
            .data(links)
            .enter()
            .append("g")
            .attr("id", "procline")
            .attr("class", "ElementProcInternalLine");
        var line_item = svg.selectAll(".ElementProcInternalLine");
        line_item.append("line")
            .attr("x1", function (d) {
            return d.x1;
        })
            .attr("y1", function (d) { return d.y1; })
            .attr("x2", function (d) { return d.x2; })
            .attr("y2", function (d) { return d.y2; })
            .attr("stroke", ProcInternalLine_Stroke);
    }
    if (proclinks.length != 0) {
        var item = svg.selectAll("g#procoutsideline")
            .data(proclinks)
            .enter()
            .append("g")
            .attr("id", "procline")
            .attr("class", "ElementProcOutSideLine");
        var line_item = svg.selectAll(".ElementProcOutSideLine");
        line_item.append("line")
            .attr("x1", function (d) {
            return d.x1;
        })
            .attr("y1", function (d) { return d.y1; })
            .attr("x2", function (d) { return d.x2; })
            .attr("y2", function (d) { return d.y2; })
            .attr("stroke", ProcOutSideLine_Stroke);
    }
    /*--render line for data--*/
    var links = [];
    if (runner.PCProcStart) {
        for (var i = 0; i < runner.PCProcStart.length; i++) {
            var procs = runner.PCProcStart[i];
            var child_links = render_runner_linkdata(ObjectList, procs);
            links = links.concat(child_links);
        }
    }
    if (links.length != 0) {
        var item = svg.selectAll("g#dataline")
            .data(links)
            .enter()
            .append("g")
            .attr("id", "dataline")
            .attr("class", "ElementDataLine");
        var line_item = svg.selectAll(".ElementDataLine");
        line_item.append("line")
            .attr("x1", function (d) {
            return d.x2;
        })
            .attr("y1", function (d) { return d.y2; })
            .attr("x2", function (d) { return d.x1; })
            .attr("y2", function (d) { return d.y1; })
            .attr("stroke", DataLine_Stroke)
            .attr("marker-end", "url(#linearrow)");
    }
}
function render_runner_collectline(ObjectList, procs) {
    var links = [];
    var proc_item = elementFromObjectList(ObjectList, procs.ObjectID);
    if (procs.InputQueue) {
        for (var j = 0; j < procs.InputQueue.length; j++) {
            var input_set = procs.InputQueue[j];
            var input_item = elementFromObjectList(ObjectList, input_set.ObjectID);
            links.push({
                "x1": input_item.PosX + input_item.Radius, "y1": input_item.PosY, "x2": proc_item.PosX, "y2": input_item.PosY
            });
        }
    }
    if (procs.OutputQueue) {
        for (var j = 0; j < procs.OutputQueue.length; j++) {
            var output_set = procs.OutputQueue[j];
            if (output_set.PCData) {
                output_set = output_set.PCData;
                var PosX = 0;
                var PosY = 0;
                var MinPosY = 0;
                var MaxPosY = 0;
                for (var m = 0; m < output_set.length; m++) {
                    var output_item = elementFromObjectList(ObjectList, output_set[m].ObjectID);
                    PosY = PosY + output_item.PosY;
                }
                PosY = PosY / output_set.length;
                for (var m = 0; m < output_set.length; m++) {
                    var output_item = elementFromObjectList(ObjectList, output_set[m].ObjectID);
                    links.push({
                        "x1": (proc_item.PosX + proc_item.Width + output_item.PosX) / 2, "y1": output_item.PosY, "x2": output_item.PosX - output_item.Radius, "y2": output_item.PosY
                    });
                    PosX = (proc_item.PosX + proc_item.Width + output_item.PosX) / 2;
                    if (m == 0)
                        MinPosY = output_item.PosY;
                    if (m == output_set.length - 1)
                        MaxPosY = output_item.PosY;
                }
                links.push({
                    "x1": proc_item.PosX + proc_item.Width, "y1": PosY, "x2": PosX, "y2": PosY
                });
                if (output_set.length != 1) {
                    links.push({
                        "x1": PosX, "y1": MinPosY, "x2": PosX, "y2": MaxPosY
                    });
                }
            }
            else {
                var output_item = elementFromObjectList(ObjectList, output_set.ObjectID);
                links.push({
                    "x1": proc_item.PosX + proc_item.Width, "y1": output_item.PosY + output_item.Height / 2, "x2": output_item.PosX, "y2": output_item.PosY + output_item.Height / 2
                });
            }
        }
    }
    if (procs.PCProcChild) {
        var prev_proc_item = elementFromObjectList(ObjectList, procs.ObjectID);
        for (var i = 0; i < procs.PCProcChild.length; i++) {
            for (var j = 0; j < procs.PCProcChild[i].length; j++) {
                var child_procs = procs.PCProcChild[i][j];
                var child_links = render_runner_collectline(ObjectList, child_procs);
                links = links.concat(child_links);
            }
        }
    }
    return links;
}
function render_runner_collectpoints(ObjectList, procs) {
    var links = [];
    var proc_item = elementFromObjectList(ObjectList, procs.ObjectID);
    if (procs.PCProcChild) {
        for (var i = 0; i < procs.PCProcChild.length; i++) {
            var prev_proc_item = elementFromObjectList(ObjectList, procs.ObjectID);
            for (var j = 0; j < procs.PCProcChild[i].length; j++) {
                var child_procs = procs.PCProcChild[i][j];
                /*--links of child_procs's child and next--*/
                var child_links = render_runner_collectpoints(ObjectList, child_procs);
                links = links.concat(child_links);
                var child_proc_item = elementFromObjectList(ObjectList, child_procs.ObjectID);
                child_links = render_runner_connectpoint(ObjectList, prev_proc_item.PosX + prev_proc_item.Width, prev_proc_item.PosY + prev_proc_item.Height / 2 + 10 * (i + 1), child_proc_item.PosX, child_proc_item.PosY + child_proc_item.Height / 2);
                links = links.concat(child_links);
                prev_proc_item = child_proc_item;
            }
        }
    }
    /*--proc next--*/
    if (procs.PCProcNext) {
        var child_proc_item = elementFromObjectList(ObjectList, procs.ObjectID);
        var proc_next_item = elementFromObjectList(ObjectList, procs.PCProcNext);
        var child_links = render_runner_connectpoint(ObjectList, child_proc_item.PosX + child_proc_item.Width, child_proc_item.PosY + child_proc_item.Height / 2, proc_next_item.PosX, proc_next_item.PosY + proc_next_item.Height / 2);
        links = links.concat(child_links);
    }
    return links;
}
function render_runner_connectpoint(ObjectList, x1, y1, x2, y2) {
    var links = [];
    if (y1 == y2) {
        links.push({
            "x1": x1, "y1": y1, "x2": x2, "y2": y2
        });
        return links;
    }
    else {
        if (x2 > x1) {
            links.push({
                "x1": x1, "y1": y1, "x2": x1 + RenderDataRadius * 8, "y2": y1
            });
            links.push({
                "x1": x1 + RenderDataRadius * 8, "y1": y1, "x2": x1 + RenderDataRadius * 8, "y2": y2
            });
            links.push({
                "x1": x1 + RenderDataRadius * 8, "y1": y2, "x2": x2, "y2": y2
            });
            return links;
        }
        else {
            links.push({
                "x1": x1, "y1": y1, "x2": x1 + RenderDataRadius * 8, "y2": y1
            });
            links.push({
                "x1": x1 + RenderDataRadius * 8, "y1": y1, "x2": x1 + RenderDataRadius * 8, "y2": y1 + RenderProcHeight / 2 + RenderVInterval / 2
            });
            links.push({
                "x1": x1 + RenderDataRadius * 8, "y1": y1 + RenderProcHeight / 2 + RenderVInterval / 2, "x2": x2 - RenderDataRadius * 8, "y2": y1 + RenderProcHeight / 2 + RenderVInterval / 2
            });
            links.push({
                "x1": x2 - RenderDataRadius * 8, "y1": y1 + RenderProcHeight / 2 + RenderVInterval / 2, "x2": x2 - RenderDataRadius * 8, "y2": y2
            });
            links.push({
                "x1": x2 - RenderDataRadius * 8, "y1": y2, "x2": x2, "y2": y2
            });
        }
        return links;
    }
}
function render_runner_linkdata(ObjectList, procs) {
    var links = [];
    if (procs.InputQueue) {
        for (var j = 0; j < procs.InputQueue.length; j++) {
            var input_set = procs.InputQueue[j];
            var input_item = elementFromObjectList(ObjectList, input_set.ObjectID);
            if (input_set.DataQueue) {
                var dataqueue = input_set.DataQueue;
                for (var n = 0; n < dataqueue.length; n++) {
                    var data_item = elementFromObjectList(ObjectList, dataqueue[n].ObjectID);
                    if (data_item) {
                        links.push({
                            "x1": input_item.PosX, "y1": input_item.PosY, "x2": data_item.PosX, "y2": data_item.PosY
                        });
                    }
                }
            }
        }
    }
    if (procs.PCProcChild) {
        for (var i = 0; i < procs.PCProcChild.length; i++) {
            for (var j = 0; j < procs.PCProcChild[i].length; j++) {
                var child_procs = procs.PCProcChild[i][j];
                var child_links = render_runner_linkdata(ObjectList, child_procs);
                links = links.concat(child_links);
            }
        }
    }
    return links;
}
window.onload = function () {
    //USEEMBEDFILE = true;
    USEEMBEDFILE = false;
    RenderProcStack = []; /*--hold pccell object, each item is {"objectid":xxx,"objectname":xxx} */
    //render_request("pcstatus.json");
    if (USEEMBEDFILE)
        render_request("/pcstatus.json");
    else {
        if (RenderProcStack.length == 0)
            render_request("/realm/status");
        else
            render_request("/realm/cellstatus/" + RenderProcStack[RenderProcStack.length - 1].objectid);
    }
};
window.onresize = function () {
    render_resize();
};
//# sourceMappingURL=app.js.map