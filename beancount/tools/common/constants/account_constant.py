ACCOUNT_EXPENSES = [
    'Expenses:Baby:BabySupplies',
    'Expenses:Baby:Clothes',
    'Expenses:Baby:Education',
    'Expenses:Baby:Food',
    'Expenses:Baby:Medical',
    'Expenses:Baby:MotherSupplies',
    'Expenses:Baby:Other',
    'Expenses:Baby:Toy',
    'Expenses:Education:SchoolFee',
    'Expenses:Entertainment',
    'Expenses:Financial:Insurance',
    'Expenses:Home:CommunityManagementFee',
    'Expenses:Home:Food',
    'Expenses:Home:Fruit',
    'Expenses:Home:Milk',
    'Expenses:Home:NetFee',
    'Expenses:Home:PhoneFee',
    'Expenses:Home:Rent',
    'Expenses:Home:Repair',
    'Expenses:Home:Snack',
    'Expenses:Home:WaterElectGas',
    'Expenses:Home:Wine',
    'Expenses:Medical:Drug',
    'Expenses:Medical:Hospital',
    'Expenses:Other:AccidentallyLost',
    'Expenses:Other:BadDebtLost',
    'Expenses:Other:Other',
    'Expenses:Other:PartyMembershipDues',
    'Expenses:Relationship:Donate',
    'Expenses:Relationship:GiftAndTreat',
    'Expenses:Relationship:Parent',
    'Expenses:Shopping:Bag',
    'Expenses:Shopping:Bathroom',
    'Expenses:Shopping:Book',
    'Expenses:Shopping:Cleaning',
    'Expenses:Shopping:Clothes',
    'Expenses:Shopping:Cosmetic',
    'Expenses:Shopping:DailySupplies',
    'Expenses:Shopping:Decoration',
    'Expenses:Shopping:Electronic',
    'Expenses:Shopping:Express',
    'Expenses:Shopping:Furniture',
    'Expenses:Shopping:Jewelry',
    'Expenses:Shopping:Kitchen',
    'Expenses:Shopping:Office',
    'Expenses:Shopping:Sport',
    'Expenses:Study',
    'Expenses:Traffic:Airplane',
    'Expenses:Traffic:Bus',
    'Expenses:Traffic:Park',
    'Expenses:Traffic:RentCar',
    'Expenses:Traffic:Repair',
    'Expenses:Traffic:Taxi',
    'Expenses:Traffic:Train',
    'Expenses:Travel:Food',
    'Expenses:Travel:Hotel',
    'Expenses:Travel:Transport',
]

ACCOUNT_INCOME = [
    'Income:Financial:Fund',
    'Income:Financial:Invest',
    'Income:Financial:YuEbao',
    'Income:Job:Bonus',
    'Income:Job:PartTime',
    'Income:Job:Salary',
    'Income:Other:Operate',
    'Income:Other:Win',
    'Income:Other:WindfallBenefit',
    'Income:Relationship:Birthday',
    'Income:Relationship:Gift',
    'Income:Relationship:Marry',
]

ACCOUNT_ASSETS = [
    'Assets:FamilySharedBalance',
    'Assets:Finance:Bound',
    'Assets:Finance:Fund',
    'Assets:Home:Balance',
    'Assets:Home:FamilyShared',
    'Assets:Loan:Pay',
    'Assets:Loan:Receive',
    'Assets:Marry',
    'Assets:Pension:Cao',
    'Assets:Pension:Huang',
    'Assets:Pocket:Husband',
    'Assets:Pocket:Wife',
    'Assets:RelationShip:Gift',
]

ALL_ACCOUNT = ACCOUNT_ASSETS + ACCOUNT_INCOME + ACCOUNT_EXPENSES
SKIP_ACCOUNT = 'SKIP' # 用于处理跳过记录
ALL_ACCOUNT.append(SKIP_ACCOUNT)