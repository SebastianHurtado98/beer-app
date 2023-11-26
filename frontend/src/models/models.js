class Customer {
    constructor(id, name) {
      this.id = id;
      this.name = name;
    }
}

class Bill {
constructor(id, customerId, total, paid, paymentType) {
    this.id = id;
    this.customerId = customerId;
    this.total = total;
    this.paid = paid;
    this.paymentType = paymentType;
}
}

function sumUnpaidBillsByCustomer(bills, customerId) {
    return bills
        .filter(bill => bill.customerId === parseInt(customerId) && !bill.paid)
        .reduce((sum, bill) => sum + parseFloat(bill.total), 0);
}

export { Customer, Bill, sumUnpaidBillsByCustomer};