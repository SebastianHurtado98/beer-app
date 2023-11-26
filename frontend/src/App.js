import React, { useState, useEffect } from 'react';
import PayButton from './components/PayButton';
import BillAmount from './components/BillAmount';
import CustomerSelector from './components/CustomerSelector';
import { getCustomers, getPendingBills } from './services/api';
import { Customer, Bill } from './models/models';
import './App.css';

function App() {
  const [customers, setCustomers] = useState([]);
  const [bills, setBills] = useState([]);
  const [selectedCustomerId, setSelectedCustomerId] = useState();
  const [refreshBills, setRefreshBills] = useState(false);

  const handleCustomerSelect = (customerId) => {
    setSelectedCustomerId(customerId);
  };

  const handleRefreshBills = () => {
    setRefreshBills(prev => !prev);
  };

  useEffect(() => {
    getCustomers().then(data => {
      const customerObjects = data.map(c => new Customer(c.id, c.name));
      setCustomers(customerObjects);
      const customerIds = customerObjects.map(c => c.id);
      getPendingBills(customerIds).then(billData => {
        const billObjects = billData.map(b => new Bill(b.id, b.customer, b.total, b.paid, b.payment_type));
        setBills(billObjects);
      }).catch(error => {
        console.error('Error al obtener bills pendientes:', error);
      });
    }).catch(error => {
      console.error('Error al obtener los clientes:', error);
    });
  }, []);

  useEffect(() => {
    const customerIds = customers.map(customer => customer.id);
    if (selectedCustomerId && customerIds.length > 0) {
      getPendingBills(customerIds).then(billData => {
        const billObjects = billData.map(b => new Bill(b.id, b.customer, b.total, b.paid, b.payment_type));
        setBills(billObjects);
      }).catch(error => {
        console.error('Error al obtener bills pendientes:', error);
      });
    }
  }, [refreshBills]);

  return (
    <div className="App min-h-screen bg-gray-800 flex justify-center items-center">
      <header className="text-white text-center">
        <CustomerSelector
          customers={customers}
          onCustomerSelect={handleCustomerSelect}
        />
        <BillAmount
          bills={bills}
          selectedCustomerId={selectedCustomerId}
        />
        <PayButton 
          selectedCustomerId={selectedCustomerId}
          onPaymentComplete={handleRefreshBills}/>
      </header>
    </div>
  );
}


export default App;