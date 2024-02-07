import * as React from 'react';
import { ThemeProvider } from '@mui/material';
import styled, {
  ThemeProvider as StyledThemeProvider,
} from 'styled-components';
import { Field, Form, Formik } from 'formik';
import { theme } from '../../../theme';
import { FormikRadioGroup } from './FormikRadioGroup';

export default {
  component: FormikRadioGroup,
  title: 'FormikRadioGroup',
};

const FieldWrapper = styled.div`
  width: 300px;
`;

const sampleChoices = [
  { name: 'Sample', value: 'sample' },
  { name: 'Choice', value: 'choice' },
];

export function RadioGroup() {
  return (
    <ThemeProvider theme={theme}>
      <StyledThemeProvider theme={theme}>
        <Formik
          initialValues={{ choiceField: sampleChoices[0].value }}
          onSubmit={(values) => {}}
        >
          {() => (
            <Form>
              <FieldWrapper>
                <Field
                  name="choiceField"
                  label="Sample label"
                  choices={sampleChoices}
                  component={FormikRadioGroup}
                />
              </FieldWrapper>
            </Form>
          )}
        </Formik>
      </StyledThemeProvider>
    </ThemeProvider>
  );
}
