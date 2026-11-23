# Independente do algoritmo: prever recebe data.frame e retorna P(Y=1).
perda_log <- function(y,p,eps=1e-15) {
 stopifnot(length(y)==length(p),all(is.finite(p)),all(p>=0&p<=1))
 q<-pmin(pmax(p,eps),1-eps)
 -mean(y*log(q)+(1-y)*log1p(-q))
}
regua_comum <- function(prever,X,y,perms,variables=names(X)) {
 stopifnot(!anyDuplicated(variables),all(variables%in%names(X)),length(variables)>=2)
 stopifnot(all(vapply(perms,function(z)identical(sort(as.integer(z)),seq_len(nrow(X))),logical(1))))
 original<-serialize(X,NULL);base<-perda_log(y,prever(X))
 delta<-function(cols) mean(vapply(perms,function(ind){
  xp<-X;xp[,cols]<-X[ind,cols,drop=FALSE];perda_log(y,prever(xp))-base
 },numeric(1)))
 individual<-setNames(vapply(variables,delta,numeric(1)),variables)
 pairs<-combn(variables,2,simplify=FALSE)
 tab<-do.call(rbind,lapply(pairs,function(ab){
  d<-delta(ab);data.frame(a=ab[1],b=ab[2],delta_ab=d,delta_a=individual[[ab[1]]],delta_b=individual[[ab[2]]],contrast=d-individual[[ab[1]]]-individual[[ab[2]]])
 }))
 stopifnot(identical(original,serialize(X,NULL)))
 tab
}
top_com_empates <- function(scores,k,tol=1e-12){
 stopifnot(all(is.finite(scores)),k>=1,k<=length(scores))
 if(max(scores)-min(scores)<=tol)return(integer())
 cutoff<-sort(scores,decreasing=TRUE)[k]
 which(scores>=cutoff-tol)
}
jaccard <- function(a,b){if(!length(a)||!length(b))return(NA_real_);length(intersect(a,b))/length(union(a,b))}
