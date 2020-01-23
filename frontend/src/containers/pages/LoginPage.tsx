import React, { useEffect } from 'react';
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
} from 'react-router-dom';
import { useMeQuery } from '../../__generated__/graphql';
import { setAuthenticated } from '../../utils/utils';
import { LOGIN_URL } from '../../config';

export function LoginPage(): React.ReactElement {
  const { data, error } = useMeQuery();
  useEffect(() => {
    if (error) {
      window.location.replace(LOGIN_URL);
    }
  });
  if (error) {
    return null;
  }
  setAuthenticated(true);
  return <Redirect to='/' />;
}
