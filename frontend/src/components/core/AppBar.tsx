import { BusinessAreaSelect } from '@containers/BusinessAreaSelect';
import { GlobalProgramSelect } from '@containers/GlobalProgramSelect';
import { UserProfileMenu } from '@containers/UserProfileMenu';
import { useCachedMe } from '@hooks/useCachedMe';
import MenuIcon from '@mui/icons-material/Menu';
import TextsmsIcon from '@mui/icons-material/Textsms';
import { Box, Button } from '@mui/material';
import MuiAppBar from '@mui/material/AppBar';
import IconButton from '@mui/material/IconButton';
import Toolbar from '@mui/material/Toolbar';
import { styled } from '@mui/system';
import * as React from 'react';
import { MiśTheme, theme } from 'src/theme';

const StyledToolbar = styled(Toolbar)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'space-between',
}));

const StyledLink = styled('a')({
  textDecoration: 'none',
  color: '#e3e6e7',
});

interface AppBarProps {
  open: boolean;
}

interface StyledAppBarProps extends AppBarProps {
  theme: MiśTheme;
}

const StyledAppBar = styled(MuiAppBar)<StyledAppBarProps>(
  ({ theme, open }) => ({
    position: 'fixed',
    top: 0,
    zIndex: theme.zIndex.drawer + 1,
    backgroundColor: theme.palette.secondary.main,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && {
      marginLeft: theme.drawer.width,
      width: `calc(100% - ${theme.drawer.width}px)`,
      transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
    }),
  }),
);

const StyledIconButton = styled(IconButton)<AppBarProps>(({ theme, open }) => ({
  marginRight: 36,
  ...(open && {
    display: 'none',
  }),
}));

export function AppBar({ open, handleDrawerOpen }): React.ReactElement {
  const { data: meData, loading: meLoading } = useCachedMe();
  const servicenow = `https://unicef.service-now.com/cc?id=sc_cat_item&sys_id=762ae3128747d91021cb670a0cbb35a7&HOPE - ${
    window.location.pathname.split('/')[2]
  }&Workspace: ${window.location.pathname.split('/')[1]} \n Url: ${
    window.location.href
  }`;

  if (meLoading) {
    return null;
  }
  return (
    <StyledAppBar theme={theme} open={open}>
      <StyledToolbar>
        <Box display="flex" alignItems="center" justifyContent="center">
          <Box ml={1}>
            <StyledIconButton
              edge="start"
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawerOpen}
              open={open}
            >
              <MenuIcon />
            </StyledIconButton>
          </Box>
          <Box display="flex" alignItems="center">
            <Box ml={6} data-cy="business-area-container">
              <BusinessAreaSelect />
            </Box>
            <Box ml={6} data-cy="global-program-filter-container">
              <GlobalProgramSelect />
            </Box>
          </Box>
        </Box>
        <Box display="flex" justifyContent="flex-end">
          <Button startIcon={<TextsmsIcon style={{ color: '#e3e6e7' }} />}>
            <StyledLink target="_blank" href={servicenow}>
              Support
            </StyledLink>
          </Button>
          <UserProfileMenu meData={meData} />
        </Box>
      </StyledToolbar>
    </StyledAppBar>
  );
}
