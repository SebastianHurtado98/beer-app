import axios from 'axios';

const apiBaseURL = 'http://localhost:8000/api';

const getCustomers = async () => {
    try {
        const response = await axios.get(`${apiBaseURL}/customers/`);
        return response.data;
    } catch (error) {
        console.error('Error al obtener los clientes:', error);
        return [];
    }
};

const getPendingBills = async (customerIds) => {
    try {
        const idString = customerIds.join(',');
        const response = await axios.get(`${apiBaseURL}/bills/list/`, {
        params: { customer_ids: idString, paid: 'False' }
        });
        return response.data;
    } catch (error) {
        console.error('Error al obtener facturas pendientes:', error);
        return [];
    }
};

const payBills = async (customerId) => {
    try {
      const response = await axios.post(`${apiBaseURL}/bills/pay/${customerId}/`);
      if (response.status === 200) {
        console.log("Facturas pagadas correctamente.")
        return response.data;
      } else if (response.status === 404) {
        console.log('No hay facturas pendientes para este cliente.');
        return null;
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        console.log('No hay facturas pendientes para este cliente.');
      } else {
        console.error('Error al pagar facturas:', error);
      }
      return null;
    }
  };

export { getCustomers, getPendingBills, payBills };