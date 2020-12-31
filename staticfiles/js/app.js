//----CSRF Token --------------------------------------//
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
var csrftoken = getCookie('csrftoken');
//------------------------------------------------------------


//---------Get current user-----------------------------------
var userid=null
    function getUser(){
        var endPoint='http://expensetracker147.herokuapp.com/api/user';
         fetch(endPoint)
        .then((resp) => resp.json())
        .then(function(data){
            console.log(data)
            userid=data.userid
            console.log('user set to',userid)
        })

    }
getUser()
//------------------------------------------------------------------//


// Listeners!
//-----------Dom string dictionary for easy access---------//
var domstring = {
    inputType:'.add__type',
    inputDescription : '.add__description',
    inputValue : '.add__value',
    inputButton : '.add__btn',
    incomeContainer: '.income__list',
    expensesContainer: '.expenses__list',
    budgetLabel: '.budget__value',
    incomeLabel: '.budget__income--value',
    expensesLabel: '.budget__expenses--value',
    percentageLabel: '.budget__expenses--percentage',
    container: '.container',
    expensesPercLabel: '.item__percentage',
    dateLabel: '.budget__title--month'

}


//-----------------------------Listeners--------------------------------------------
function setUpListeners(){
    //adding item => submit btn
    document.querySelector(domstring.inputButton).addEventListener('click',addItem);
    document.addEventListener('keypress',keypress)
    document.querySelector(domstring.inputType).addEventListener('change',typeChange);
    document.querySelector(domstring.container).addEventListener('click',DeleteItem);
}
setUpListeners()

//----Listeners func-----------------------------//
function addItem(event){
    console.log('print click button clicked')
    if(userid==null){window.location.href='http://expensetracker147.herokuapp.com/login'}
    var type,desc,value,url
    type=document.querySelector(domstring.inputType).value,
    desc=document.querySelector(domstring.inputDescription).value,
    value=parseFloat(document.querySelector(domstring.inputValue).value)
    console.log(type,desc,value)
    //post method
    if (type === 'inc')
    {
        url = 'http://expensetracker147.herokuapp.com/api/income'
        obj={'IncomeValue':value,'Description':desc,'user':userid}
    }
    else
    {
        url = 'http://expensetracker147.herokuapp.com/api/expense'
        obj={'ExpenseValue':value,'Description':desc,'user':userid}
    }
    
    bodyval =JSON.stringify(obj)
    console.log(bodyval)
    fetch(url, {
        method:'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:bodyval
    }
    ).then(function(response){
        
        console.log('posted!')
        //Re-fetching the values!
        reset()
        callGetter()
    })
}
function typeChange(){
    console.log('type was changed!')
}
function keypress(event){
    if (event.key==="Enter")
        {
            console.log('Enter key was pressed!')
            addItem()
        }
}



//-----------------------Get data and display here!-------------------------------------------
function getIncome(){
    var IncomeEndPoint='http://expensetracker147.herokuapp.com/api/income'
    fetch(IncomeEndPoint)
    .then((resp) => resp.json())
    .then(function(incomeData)
    {
        console.log('incomedata:',incomeData)
        var html,element;
        publicIncomeData = incomeData
        element = domstring.incomeContainer;
        for (var income in incomeData)
        {
            console.log(income)
            html = '<div class="item clearfix" id="inc-%id%"> <div class="item__description">%description%</div><div class="right clearfix"><div class="item__value">%value%</div><div class="item__delete"><button class="item__delete--btn"><i class="ion-ios-close-outline"></i></button></div></div></div>';
            newHtml = html.replace('%id%',income)
            newHtml = newHtml.replace('%description%',incomeData[income].Description)
            newHtml = newHtml.replace('%value%',parseFloat(incomeData[income].IncomeValue))
            document.querySelector(element).insertAdjacentHTML('beforeend', newHtml)
        }
        return incomeData
    })
        

}

function getExpense(){
    var expenseEndPoint='http://expensetracker147.herokuapp.com/api/expense'
    var returnVal;
    fetch(expenseEndPoint)
    .then((resp) => resp.json())
    .then(function(expenseData){
        console.log('expense data :',expenseData)
        var html,element;
        publicExpenseData = expenseData
        element = domstring.expensesContainer;
        for (var expense in expenseData)
        {
            console.log(expense)
            html = '<div class="item clearfix" id="exp-%id%"><div class="item__description">%description%</div><div class="right clearfix"><div class="item__value">%value%</div><div class="item__percentage">%percentage%</div><div class="item__delete"><button class="item__delete--btn"><i class="ion-ios-close-outline"></i></button></div></div></div>'
            newHtml = html.replace('%id%',expense)
            newHtml = newHtml.replace('%description%',expenseData[expense].Description)
            newHtml = newHtml.replace('%value%',expenseData[expense].ExpenseValue)
            newHtml = newHtml.replace('%percentage%',expenseData[expense].ExpensePercentage)
            document.querySelector(element).insertAdjacentHTML('beforeend', newHtml)
        } 
    })
}

function getTotal(){
    var totalEndPoint='http://expensetracker147.herokuapp.com/api/totaldata'
    fetch(totalEndPoint)
    .then((resp) => resp.json())
    .then(function(totalData){
        console.log('totalData',totalData[0].TotalBudget)
        document.querySelector(domstring.budgetLabel).textContent=totalData[0].TotalBudget
        document.querySelector(domstring.incomeLabel).textContent = totalData[0].TotalIncome
        document.querySelector(domstring.expensesLabel).textContent =totalData[0].TotalExpense
        document.querySelector(domstring.percentageLabel).textContent=totalData[0].Percentage
    })

}
var publicIncomeData,publicExpenseData;
function callGetter(){
    publicExpenseData=getExpense()
    publicIncomeData=getIncome()
    getTotal()
    displayMonth()
}
callGetter()
function reset(){
        document.querySelector(domstring.incomeContainer).innerHTML=''
        document.querySelector(domstring.expensesContainer).innerHTML=''
        document.querySelector(domstring.budgetLabel).textContent=''
        document.querySelector(domstring.incomeLabel).textContent = ''
        document.querySelector(domstring.expensesLabel).textContent =''
        document.querySelector(domstring.percentageLabel).textContent=''
}
function displayMonth(){
    var now, months, month, year;
    
    now = new Date();
    //var christmas = new Date(2016, 11, 25);
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    month = now.getMonth();
    
    year = now.getFullYear();
    document.querySelector(domstring.dateLabel).textContent = months[month] + ' ' + year;
}
function DeleteItem(event){
    var itemID, splitID, type, ID,dataobj,url
        
    itemID = event.target.parentNode.parentNode.parentNode.parentNode.id
    console.log('delete button clicked!',itemID)
    splitID = itemID.split('-')
    type = splitID[0]
    ID = parseInt(splitID[1])
    if (type=='exp')
    {
        dataobj = publicExpenseData
        url=`http://expensetracker147.herokuapp.com/api/deleteExpense/${dataobj[ID].id}`
    }
    else
    {
        dataobj = publicIncomeData
        url=`http://expensetracker147.herokuapp.com/api/deleteIncome/${dataobj[ID].id}`
    }
    console.log('select item',dataobj[ID])
    console.log(url)
    fetch(url, 
    {
				method:'DELETE', 
				headers:{
					'Content-type':'application/json',
					'X-CSRFToken':csrftoken,
				}
			}).then((response) => {
                reset()
                callGetter()
            })
}
            