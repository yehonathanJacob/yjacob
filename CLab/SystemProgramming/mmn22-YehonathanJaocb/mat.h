typedef struct mat * pmat;

pmat create_mat();
void delete_mat(pmat);

void read_mat(pmat, double *, int);
void print_mat(pmat);
void add_mat(pmat,pmat,pmat *);
void sub_mat(pmat,pmat,pmat *);
void mul_mat(pmat,pmat,pmat *);
void mul_scalar(pmat,double,pmat *);
void trans_mat(pmat,pmat *);