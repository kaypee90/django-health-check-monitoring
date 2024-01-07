import React, { Fragment } from 'react';
import Container from '@mui/material/Container';
import HealthCheckTable from './health-check-table';
import NavigationAppBar from './navigation-bar';
import { createTheme, ThemeProvider, styled } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

import { HealthCheckSummary } from '../models/index';
import { getHealthCheckCountData } from '../api';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const theme = createTheme();

theme.typography.h3 = {
  fontSize: '1.2rem',
  '@media (min-width:600px)': {
    fontSize: '1.5rem',
  },
  [theme.breakpoints.up('md')]: {
    fontSize: '2.4rem',
  },
};

export default function Dashboard() {
  const workingStatusId = 1

  const [summaries, setSummaries] = React.useState<HealthCheckSummary[]>([])
  const [totalCount, setTotalCount] = React.useState<number>(0)
  const [totalFailed, setTotalFailed] = React.useState<number>(0)

  const createHealthCheckSummary = (
        name: string,
        statusId: number,
        count: number,
    ): HealthCheckSummary  => {
      const status = statusId === workingStatusId ? 'Working' : "Failing";
      return { name, statusId, status, count };
    }

  const fetchData = React.useCallback(async () => {
    let failed = 0;
    let total = 0
    let healthCheckSummaries: HealthCheckSummary[] = [];
    const response = await getHealthCheckCountData();

    response.data.forEach((item, _) => {
        total += item.count

        if (item.status !== workingStatusId) {
          failed += item.count
        }

        const summary = createHealthCheckSummary(item.name, item.status, item.count)
        healthCheckSummaries.push(summary)
    })


    setSummaries(healthCheckSummaries)
    setTotalCount(total)
    setTotalFailed(failed)

  }, []);
    
  React.useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    fetchData()
  }, [fetchData])


  return (
    <Fragment>
        <NavigationAppBar />
        <Container>
         <br />
         <br />
         <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3}}>
            <Grid item xs={6}>
              <Item>
                <ThemeProvider theme={theme}>
                      <Typography variant="h3">Failed Checks</Typography>
                      <Typography variant="h3">{totalFailed}</Typography>
                </ThemeProvider>
              </Item>
            </Grid>
            <Grid item xs={6}>
              <Item>
                <ThemeProvider theme={theme}>
                      <Typography variant="h3">Total Checks</Typography>
                      <Typography variant="h3">{totalCount}</Typography>
                </ThemeProvider>
              </Item>
            </Grid>
          </Grid>
         <br />
         <br />
          <HealthCheckTable summaries={summaries}/>
      </Container>
    </Fragment>
  );
}