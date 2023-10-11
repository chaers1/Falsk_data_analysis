
// 获取分析类型下拉框和日期输入框元素
var analysisTypeDropdown = document.getElementById("analysis_type");
var singleDayInput = document.getElementById("single_day_input");
var multiDayInput = document.getElementById("multi_day_input");

// 添加事件监听器，根据用户选择显示或隐藏日期输入框
analysisTypeDropdown.addEventListener("change", function () {
    if (analysisTypeDropdown.value === "single_day") {
        singleDayInput.style.display = "block";
        multiDayInput.style.display = "none";
    } else if (analysisTypeDropdown.value === "multi_day") {
        singleDayInput.style.display = "none";
        multiDayInput.style.display = "block";
    } else {
        singleDayInput.style.display = "none";
        multiDayInput.style.display = "none";
    }
});
function showTable() {
    var tableContainer = document.querySelector('.analysis-table-container');
    var closeButton = document.querySelector('.analysis-clost-button');
    var h3Element = document.querySelector('.analysis_div_h3');
    var analysisTypeDropdown = document.getElementById("analysis_type");

    // 显示表格
    tableContainer.style.display = 'block';

    // 显示按钮
    closeButton.style.display = 'block';

    // 根据用户选择的分析类型来显示或隐藏H3标题
    if (analysisTypeDropdown.value === "single_day" || analysisTypeDropdown.value === "multi_day") {
        h3Element.style.display = 'block';
    } else {
        h3Element.style.display = 'none';
    }
}

// 调用showTable函数以显示表格及相关元素
showTable();

function closeFileList() {
  var fileList = document.querySelector('.analysis_div_button');
  fileList.style.display = 'none';
  var closeButton = document.querySelector('.analysis-clost-button');
  closeButton.style.display = 'block';
  // 清除 div 元素中的内容
  fileList.innerHTML = '';
}