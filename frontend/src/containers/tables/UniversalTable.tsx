import React, { ReactElement, useState, useEffect } from 'react';
import { Order, TableComponent } from '../../components/table/TableComponent';
import { HeadCell } from '../../components/table/EnhancedTableHead';
import { columnToOrderBy } from '../../utils/utils';

interface UniversalTableProps<T, K> {
  rowsPage?: number[];
  initialVariables: K;
  query;
  queriedObjectName: string;
  renderRow: (row: T) => ReactElement;
  headCells: HeadCell<T>[];
  title: string;
}
export function UniversalTable<T, K>({
  rowsPage = [5, 10, 15],
  initialVariables,
  query,
  queriedObjectName,
  renderRow,
  headCells,
  title,
}: UniversalTableProps<T, K>): ReactElement {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(rowsPage[0]);
  const [orderBy, setOrderBy] = useState(null);
  const [orderDirection, setOrderDirection] = useState('asc');
  const { data, refetch, loading } = query({
    variables: { ...initialVariables, first: rowsPerPage },
    fetchPolicy: 'network-only',
  });

  useEffect(() => {
    if (initialVariables) {
      setPage(0);
    }
  }, [initialVariables]);

  if (!data) {
    return null;
  }

  const { edges } = data[queriedObjectName];
  const typedEdges = edges.map((edge) => edge.node as T);
  console.log('query1', typedEdges, initialVariables);
  return (
    <TableComponent<T>
      title={title}
      data={typedEdges}
      loading={loading}
      renderRow={renderRow}
      headCells={headCells}
      rowsPerPageOptions={rowsPage}
      rowsPerPage={rowsPerPage}
      page={page}
      itemsCount={data[queriedObjectName].totalCount}
      handleChangePage={(event, newPage) => {
        const variables = {
          first: undefined,
          last: undefined,
          after: undefined,
          before: undefined,
          orderBy: undefined,
        };
        if (newPage < page) {
          variables.last = rowsPerPage;
          variables.before = edges[0].cursor;
        } else {
          variables.after = edges[edges.length - 1].cursor;
          variables.first = rowsPerPage;
        }
        if (orderBy) {
          variables.orderBy = columnToOrderBy(orderBy, orderDirection);
        }
        setPage(newPage);
        refetch(variables);
      }}
      handleChangeRowsPerPage={(event) => {
        const value = parseInt(event.target.value, 10);
        setRowsPerPage(value);
        setPage(0);
        const variables = {
          first: value,
          last: undefined,
          before: undefined,
          after: undefined,
          orderBy: undefined,
        };
        if (orderBy) {
          variables.orderBy = columnToOrderBy(orderBy, orderDirection);
        }
        refetch(variables);
      }}
      handleRequestSort={(event, property) => {
        let direction = 'asc';
        if (property === orderBy) {
          direction = orderDirection === 'asc' ? 'desc' : 'asc';
        }
        setOrderBy(property);
        setOrderDirection(direction);
        refetch({
          last: undefined,
          before: undefined,
          after: undefined,
          first: rowsPerPage,
          orderBy: columnToOrderBy(property, direction),
        });
      }}
      orderBy={orderBy}
      order={orderDirection as Order}
    />
  );
}
