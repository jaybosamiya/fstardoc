(** [c_True] is the singleton inductive type---it is trivially
    inhabited. Like [c_False], [c_True] is seldom used. We instead use
    its "squashed" variants, [True] *)
type c_True = | T

(** Produce equality as a [Type] if provable from context. *)
val get_equality
  (#t:Type)
  (a b: t)
  : Pure (a == b)
    (requires (a == b))
    (ensures (fun _ -> True))

(** [l_True] has a special bit of syntactic sugar. It is written just
    as "True" and rendered in the ide as [True]. It is a squashed version
    of constructive truth, [c_True]. *)
[@"tac_opaque" smt_theory_symbol]
let l_True :logical = squash c_True
