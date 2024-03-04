import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import styled from 'styled-components';
import { useField } from 'formik';
import { useSnackbar } from '@hooks/useSnackBar';
import { useTranslation } from 'react-i18next';

interface DropzoneContainerProps {
  disabled?: boolean;
}
const DropzoneContainer = styled.div<DropzoneContainerProps>`
  width: 100%;
  height: 100px;
  background-color: rgba(2, 62, 144, 0.1);
  color: #023e90;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.5px;
  line-height: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: ${({ theme }) => theme.spacing(5)};
  cursor: pointer;
  ${({ disabled }) => (disabled ? 'filter: grayscale(100%);' : '')}
`;

export function DropzoneField({ loading }): React.ReactElement {
  const [, , helpers] = useField('file');
  const { t } = useTranslation();
  const { showMessage } = useSnackbar();
  const onDrop = useCallback(
    (acceptedFiles) => {
      // Log the MIME types of the accepted files
      acceptedFiles.forEach((file) => {
        console.log(file.type);
      });

      if (acceptedFiles.length !== 1) {
        return;
      }
      const file = acceptedFiles[0];
      const fileSizeMB = file.size / (1024 * 1024);
      if (fileSizeMB > 200) {
        showMessage(
          `${t('File size is to big. It should be under 200MB')}, ${t(
            'File size is',
          )} ${fileSizeMB}MB`,
        );
        return;
      }
      helpers.setValue(file);
    },
    [helpers, showMessage, t],
  );
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    disabled: loading,
    //@ts-ignore
    accept: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    onDrop,
  });

  const acceptedFilename =
    acceptedFiles.length > 0 ? acceptedFiles[0].name : null;
  return (
    <div>
      <DropzoneContainer {...getRootProps()} disabled={loading}>
        <input {...getInputProps()} data-cy="file-input" />
        {acceptedFilename || 'UPLOAD FILE'}
      </DropzoneContainer>
    </div>
  );
}
