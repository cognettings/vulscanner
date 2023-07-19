import Router from 'next/router'
import RegisterService from 'services/RegisterService';

const Test = ({ props }) => {
  let token;
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const status = await RegisterService.updateUserData(token);
      debugger
    } catch (error) {
        Router.push('/500');
    }
  };
};
