import { Box, Button, DialogContent, DialogTitle } from '@material-ui/core';
import React, { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import styled from 'styled-components';
import { useImportedIndividualFlexFieldsQuery } from '../../../../__generated__/graphql';
import { Dialog } from '../../../dialogs/Dialog';
import { DialogActions } from '../../../dialogs/DialogActions';

const DialogTitleWrapper = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
`;

const DialogFooter = styled.div`
  padding: 12px 16px;
  margin: 0;
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  text-align: right;
`;

const StyledImage = styled.img`
  max-width: 100%;
  max-height: 100%;
`;

const MiniImage = styled.img`
  height: 45px;
  width: 45px;
  cursor: pointer;
`;

export const StyledLink = styled(Link)`
  color: #000;
`;

export const ImportedIndividualFlexFieldPhotoModal = ({
  field,
}): React.ReactElement => {
  const { id } = useParams();
  const { data } = useImportedIndividualFlexFieldsQuery({
    variables: { id },
    fetchPolicy: 'network-only',
  });
  const [dialogOpen, setDialogOpen] = useState(false);

  if (!data) {
    return null;
  }

  const { flexFields } = data.importedIndividual;
  const picUrl = flexFields[field.name];

  return (
    <>
      <MiniImage alt='photo' src={picUrl} onClick={() => setDialogOpen(true)} />
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        aria-labelledby='form-dialog-title'
      >
        <DialogTitleWrapper>
          <DialogTitle id='scroll-dialog-title'>Photo</DialogTitle>
        </DialogTitleWrapper>
        <DialogContent>
          <Box p={3}>
            <StyledImage alt='photo' src={picUrl} />
          </Box>
        </DialogContent>
        <DialogFooter>
          <DialogActions>
            <Button onClick={() => setDialogOpen(false)}>CANCEL</Button>
          </DialogActions>
        </DialogFooter>
      </Dialog>
    </>
  );
};
