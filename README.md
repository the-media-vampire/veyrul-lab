# Restricted private-tag filter

Run `python3 test_filter.py`. Stage one UTF-8 file with `python3 filter_private.py < input.twee > staged.twee`; check exit status before compiling. Never redirect onto the input path. No dependencies beyond Python's standard library.

The filter function and nine assertions were exercised in isolated Python execution receipt 08414aea-13a8-44dc-8f0b-75864a90a2ae; the published files and stdin wrapper have not separately been executed. No Tweego/VS Code build was run.

Comparison receipt 9b31588d-bce9-46c7-bece-e74803cf8d1d tested Theo's loop fragment using sh -n (exit 2: redirection unexpected) and his exact substring filter (4/6 expectations passed). EOF without a trailing newline worked; exact-tag and title-only mentions were wrongly deleted.

This deliberately changed experiment tests only a supported subset, not all Twee syntax. Metadata headers are refused, including otherwise valid metadata syntax. Lines beginning :: are treated as headers. Escapes, full grammar, cross-file semantics, links to omitted passages, asset copying and config parsing are outside scope. Test against a pinned compiler before deployment. This is not a confidentiality boundary.

Interface: UTF-8 text in/out, exact case-sensitive Twine.private tag, preamble preserved, unsupported header raises before output. Extend using a grammar-backed parser and fixtures rather than relaxing the regex blindly.

Source basis: art_01M6CR2K2FYD0F71ZB5SPNR2AA revision 1 documents omission and unresolved release status. Extension MIT naming does not establish Tweego/story-format licenses. This original package is MIT; it does not bundle either dependency.