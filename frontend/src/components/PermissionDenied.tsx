import React from 'react';
import styled from 'styled-components';
import { Box, Paper } from '@material-ui/core';
import BlockRoundedIcon from '@material-ui/icons/BlockRounded';

const Container = styled.div`
  padding: 20px;
`;
const Icon = styled(BlockRoundedIcon)`
  && {
    font-size: 100px;
  }
`;
const PaperContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: rgba(0, 0, 0, 0.38);
  padding: 70px;
  font-size: 50px;
  height: calc(100vh - 104px);
`;
const SmallerText = styled.div`
  font-size: 16px;
`;

export function PermissionDenied(): React.ReactElement {
  return (
    <Container>
      <Paper>
        <PaperContainer>
          <Icon />
          <Box>Permission Denied</Box>
          <SmallerText>
            Ask the Administrator to get access to this page
          </SmallerText>
        </PaperContainer>
      </Paper>
    </Container>
  );
}
