#!/bin/bash
# Gate for the Lean formalisation. It passes only if all of these hold:
#  * the sources contain no `sorry`, `admit`, `native_decide`, `axiom` keyword (anywhere,
#    including one on a line of its own), `#eval`, `run_cmd`, `initialize`, `IO`, `set_option`,
#    or syntax-extension commands (`macro`, `elab`, `syntax`, `notation`, `import Lean`, ...),
#    which could redefine `#print axioms`;
#  * the library builds without errors;
#  * the gate itself (not a file in the repo) generates the `#print axioms` report for each
#    REQUIRED declaration, and each report is present exactly once;
#  * each REQUIRED declaration (with its transitive dependencies) uses only Lean's standard axioms
#    (propext, Classical.choice, Quot.sound).
# REQUIRED lists every declaration cited in the accompanying paper, plus the declarations queried
# during development; names are fully qualified. Definitions may use a subset of the three axioms.
# Trust boundary: the token filter is a heuristic over the project's .lean sources. The gate assumes
# the pinned toolchain, Mathlib and lake configuration are unmodified. It is not a sandbox, and it
# does not audit declarations other than the REQUIRED ones.
# Lean wraps long axiom lists across several lines, so the output is flattened before parsing.
export PATH="$HOME/.elan/bin:$PATH"
cd "$(dirname "$0")" || exit 1
LIB="Dandelin"
REQUIRED="Dandelin.abs_lt_of_both_nappes Dandelin.apexRho Dandelin.apex_gen_mem Dandelin.apex_section_R3 Dandelin.apex_section_line Dandelin.apex_section_point Dandelin.apex_section_two_lines Dandelin.apex_two_lines_subset Dandelin.between_of_gram Dandelin.bounded_iff Dandelin.cone2 Dandelin.cone_outside_sphere Dandelin.cone_tangent_sq Dandelin.converse_alg Dandelin.dandelin Dandelin.dandelin_converse Dandelin.dandelin_exists Dandelin.dandelin_hyperbola Dandelin.dandelin_of_between_isTangentAt Dandelin.decomp_of_finrank_le_three Dandelin.directrix_converse Dandelin.directrix_converse_nappe Dandelin.directrix_ellipse Dandelin.directrix_iff_ellipse Dandelin.directrix_iff_hyperbola Dandelin.directrix_iff_parabola Dandelin.directrix_parabola Dandelin.dist_eq_of_isTangentAt Dandelin.dist_tangencyPoint Dandelin.dist_tangent_eq Dandelin.ecc Dandelin.ecc_eq_one Dandelin.ecc_lt_one_iff Dandelin.ellipse_nonempty Dandelin.ellipse_regime Dandelin.ellipse_regime_iff Dandelin.eq_of_mem_both_nappes Dandelin.exists_generator_of_mem_cone Dandelin.exists_unit_orth Dandelin.focal_dist_eq_div Dandelin.focal_dist_eq_ecc_mul Dandelin.focal_dist_eq_ecc_mul_abs Dandelin.focal_dist_eq_ecc_mul_lower Dandelin.focal_dist_eq_infDist_axisPlane Dandelin.focal_sq Dandelin.focus₁_eq_proj Dandelin.focus₂_eq_proj Dandelin.gen_point Dandelin.generator_mem_cone Dandelin.hyp_between Dandelin.hyp_both_nappes Dandelin.hyp_converse Dandelin.hyp_lower Dandelin.hyp_param_sub Dandelin.hyp_tangent_iff Dandelin.hyp_upper Dandelin.hyperbola_regime_iff Dandelin.infDist_axisPlane Dandelin.infDist_axisPlane_eq_mul Dandelin.infDist_directrix Dandelin.isTangentAt_focus₁ Dandelin.isTangentAt_focus₂ Dandelin.isTangentAt_tangencyPoint Dandelin.mem_cone2_iff Dandelin.mem_cone2_iff_angle Dandelin.mem_cone2_iff_focal_directrix Dandelin.mem_cone_iff_angle Dandelin.mem_cone_iff_of_normalised Dandelin.mem_plane_iff Dandelin.one_lt_ecc_iff Dandelin.one_nappe Dandelin.parabola_regime Dandelin.plane Dandelin.plane_eq_mk' Dandelin.proj_mem_plane Dandelin.regime_R3 Dandelin.section_bounded Dandelin.section_unbounded Dandelin.tangencyPoint_mem_axisPlane Dandelin.tangencyPoint_mem_line Dandelin.tangencyPoint_mem_sphere Dandelin.tangencyPoint_perp Dandelin.tangent_iff Dandelin.tangent_lengths_eq Dandelin.tangent_of_proj Dandelin.l14_mem_cone_iff Dandelin.l14_mem_cone2_iff Dandelin.l14_isTangentAt_plane Dandelin.l14_isTangent_plane_iff Dandelin.l14_directrix_eq Dandelin.l14_dandelin_ellipse Dandelin.l14_inscribed Dandelin.l14_dandelin_hyperbola Dandelin.l14_directrix_ellipse Dandelin.l14_parabola Dandelin.l14_regime_R3 Dandelin.l14_apex_R3 Dandelin.l14w_dandelin_ellipse Dandelin.l14w_dandelin_hyperbola Dandelin.l14w_parabola Dandelin.l14w_apex Dandelin.l14w_regime_inscribed Dandelin.Classical.l15_inner_self Dandelin.Classical.l15_unit Dandelin.Classical.l15_plane_normal Dandelin.Classical.l15_planeAxisAngle Dandelin.Classical.l15_cone_eq Dandelin.Classical.l15_generator_param Dandelin.Classical.l15_generator_of_unit Dandelin.Classical.l15_plane_sphere Dandelin.Classical.l15_plane_sphere_conv Dandelin.Classical.l15_line_mem Dandelin.Classical.l15_line_sphere Dandelin.Classical.l15_ks Dandelin.Classical.l15_tangent_cone_iff Dandelin.Classical.l15_vnot Dandelin.Classical.l15_m_sq_le Dandelin.Classical.l15_regime_ell Dandelin.Classical.l15_regime_hyp Dandelin.Classical.l15_regime_par Dandelin.Classical.l15_noncirc Dandelin.Classical.l15_S Dandelin.Classical.l15_dandelin_data Dandelin.Classical.l15_mk_dandelin Dandelin.Classical.l15_two_roots Dandelin.Classical.l15_sOppSide Dandelin.Classical.l15_inside_pos Dandelin.Classical.l15_inside_neg Dandelin.Classical.l15_gen_on_sphere Dandelin.Classical.l15_gen_segment Dandelin.Classical.l15_plane_dir Dandelin.Classical.l15_isGreatest Dandelin.Classical.l15_orient Dandelin.Classical.l15_sigma_sq Dandelin.Classical.l15_center Dandelin.Classical.l15_S_eq Dandelin.Classical.l15_cone2_sigma Dandelin.Classical.l15_dandelin_iff Dandelin.Classical.l15_data' Dandelin.Classical.l15_ell_pkg Dandelin.Classical.l15_setup Dandelin.Classical.cov_Conics1_a Dandelin.Classical.l15_gen_segment' Dandelin.Classical.cov_Conics1_b Dandelin.Classical.l15_hyp_pkg Dandelin.Classical.cov_Conics2_a Dandelin.Classical.l15_cone_of_double Dandelin.Classical.l15_cone_of_double_neg Dandelin.Classical.l15_inner_u Dandelin.Classical.cov_Conics2_b Dandelin.Classical.l15_circle_pt Dandelin.Classical.l15_span_circle Dandelin.Classical.l15_directrix_eq Dandelin.Classical.cov_Conics3_obligation Dandelin.Classical.l15_ecc_eq Dandelin.Classical.cov_Conics3_a Dandelin.Classical.cov_Conics3_b Dandelin.Classical.cov_Conics3_parabola_unique"
SOURCES="$(find $LIB -name '*.lean' | sort | tr '\n' ' ') $LIB.lean"
[ -e .lake/packages/mathlib ] || lake exe cache get || { echo "FAIL: could not fetch Mathlib cache"; exit 1; }
if grep -nE "\bsorry\b|\badmit\b|native_decide|\baxiom\b|#eval|\brun_cmd\b|\binitialize\b|\bIO\b|\bdebug\.|\bmacro|\belab|\bsyntax\b|\bnotation\b|\binfix|\bprefix\b|\bpostfix\b|import Lean|open Lean|\bset_option\b" $SOURCES; then
  echo "FAIL: forbidden token"; exit 1; fi
build=$(lake build $LIB 2>&1); bstatus=$?
printf '%s\n' "$build" | tail -3
[ "$bstatus" -eq 0 ] || { printf '%s\n' "$build"; echo "FAIL: build"; exit 1; }
chk=".gatecheck_$$.lean"
trap 'rm -f "$chk"' EXIT
{ echo "import $LIB"; for t in $REQUIRED; do echo "#print axioms $t"; done; } > "$chk"
out=$(lake env lean "$chk" 2>&1); status=$?
printf '%s\n' "$out"
[ "$status" -eq 0 ] || { echo "FAIL: axiom report"; exit 1; }
echo "$out" | grep -qE "(^|:)[[:space:]]*error" && { echo "FAIL: Lean reported an error"; exit 1; }
flat=$(printf '%s\n' "$out" | awk '/^'"'"'/{if(buf!="")print buf; buf=$0; next} {buf=buf" "$0} END{if(buf!="")print buf}')
reports=$(printf '%s\n' "$flat" | grep -E "depends on axioms|does not depend on any axioms")
n=0
for t in $REQUIRED; do
  te=$(printf '%s' "$t" | sed 's/[.]/\\./g')
  c=$(printf '%s\n' "$reports" | grep -cE "^'$te' (depends on axioms|does not depend)")
  [ "$c" -eq 1 ] || { echo "FAIL: expected one axiom report for $t, found $c"; exit 1; }
  n=$((n+1))
done
[ "$(printf '%s\n' "$reports" | grep -c .)" -eq "$n" ] || { echo "FAIL: unexpected extra reports"; exit 1; }
printf '%s\n' "$reports" | grep "depends on axioms" | grep -qv '\]' && { echo "FAIL: unterminated axiom list"; exit 1; }
bad=$(printf '%s\n' "$reports" | grep "depends on axioms" | sed 's/.*depends on axioms: *\[//; s/\].*//' \
      | tr ',' '\n' | sed 's/^ *//; s/ *$//' | grep -v '^$' | sort -u \
      | grep -vE '^(propext|Classical\.choice|Quot\.sound)$')
[ -n "$bad" ] && { echo "FAIL: nonstandard axioms: $bad"; exit 1; }
echo "PASS ($n declarations, standard axioms only)"
