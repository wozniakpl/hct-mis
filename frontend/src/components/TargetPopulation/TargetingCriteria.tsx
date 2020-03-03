import React from 'react';
import styled from 'styled-components';
import { useTranslation } from 'react-i18next';
import { Typography, Paper } from '@material-ui/core';
import { Criteria } from './Criteria';

const data = [
  {
    intakeGroup: 'Children 9/10/2019',
    sex: 'Female',
    age: '7 - 15 years old',
    distanceToSchool: 'over 3km',
    household: 'over 5 individuals',
  },
  {
    intakeGroup: 'Children 9/10/2019',
    sex: 'Male',
    age: null,
    distanceToSchool: 'over 3km',
    household: null,
  },
];

const PaperContainer = styled(Paper)`
  padding: ${({ theme }) => theme.spacing(3)}px
    ${({ theme }) => theme.spacing(4)}px;
  margin: ${({ theme }) => theme.spacing(5)}px;
  border-bottom: 1px solid rgba(224, 224, 224, 1);
`;

const Title = styled.div`
  padding-bottom: ${({ theme }) => theme.spacing(2)}px;
`;

const ContentWrapper = styled.div`
  display: flex;
`;

const Divider = styled.div`
  border-left: 1px solid #b1b1b5;
  margin: 0 ${({ theme }) => theme.spacing(10)}px;
  position: relative;
`;

const DividerLabel = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  font-weight: 500;
  color: #253b46;
  text-transform: uppercase;
  padding: 5px;
  border: 1px solid #b1b1b5;
  border-radius: 50%;
  background-color: #fff;
`;

export function TargetingCriteria() {
  const { t } = useTranslation();

  return (
    <div>
      <PaperContainer>
        <Title>
          <Typography variant='h6'>{t('Targeting Criteria')}</Typography>
        </Title>
        <ContentWrapper>
          {data.map((criteria, index) => {
            return (
              <>
                <Criteria criteria={criteria} />{' '}
                {index % 2 ? null : (
                  <Divider>
                    <DividerLabel>Or</DividerLabel>
                  </Divider>
                )}
              </>
            );
          })}
        </ContentWrapper>
      </PaperContainer>
    </div>
  );
}
