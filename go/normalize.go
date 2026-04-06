package kairos

// nativePagination constructs a Pagination from native worker response fields.
// Workers return: count, total, hasMore (camelCase), limit, offset — rather
// than the SDK's page-based Pagination envelope.
func nativePagination(total, limit, offset int, hasMore bool) *Pagination {
	page := 1
	if limit > 0 {
		page = offset/limit + 1
	}
	return &Pagination{
		Page:    page,
		Limit:   limit,
		Total:   total,
		HasMore: hasMore,
	}
}

// computedPagination is like nativePagination but infers hasMore when the
// worker doesn't return an explicit hasMore/has_more field (e.g. documents and
// whiteboards only return total_count).
func computedPagination(total, limit, offset, returned int) *Pagination {
	page := 1
	if limit > 0 {
		page = offset/limit + 1
	}
	hasMore := total > 0 && (offset+returned) < total
	return &Pagination{
		Page:    page,
		Limit:   limit,
		Total:   total,
		HasMore: hasMore,
	}
}
