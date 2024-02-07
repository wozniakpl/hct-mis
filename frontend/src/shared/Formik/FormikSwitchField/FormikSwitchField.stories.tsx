import * as React from 'react';
import { ThemeProvider } from '@mui/material';
import styled, {
  ThemeProvider as StyledThemeProvider,
} from 'styled-components';
import { Field, Form, Formik } from 'formik';
import { theme } from '../../../theme';
import { FormikSwitchField } from './FormikSwitchField';

export default {
  component: FormikSwitchField,
  title: 'FormikSwitchField',
};

const FieldWrapper = styled.div`
  width: 300px;
`;

export function SwitchField() {
  return (
    <ThemeProvider theme={theme}>
      <StyledThemeProvider theme={theme}>
        <Formik
          initialValues={{ switchField: false }}
          onSubmit={(values) => console.log(values)}
        >
          {() => (
            <Form>
              <FieldWrapper>
                <Field
                  name="switchField"
                  label="Switch field"
                  color="primary"
                  component={FormikSwitchField}
                />
              </FieldWrapper>
            </Form>
          )}
        </Formik>
      </StyledThemeProvider>
    </ThemeProvider>
  );
}
