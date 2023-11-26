import { useState, useEffect } from 'react';
import { getCustomers, getPendingBills } from '../services/api';
import { Customer, Bill } from '../models/models';

const useInitialDataLoad = () => {
  const [customers, setCustomers] = useState([]);
  const [bills, setBills] = useState([]);

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

  return { customers, bills };
};

export default useInitialDataLoad;
